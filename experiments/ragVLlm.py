from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import JsonOutputParser
import tiktoken
from thefuzz import process
from termcolor import colored

prompt = """
You are an assistant for creating JSON representations of fictional characters. Identify the following information for the character:
1. Name
2. Hair Color
3. House
4. Wand Size In Inches
5. Pet Type

using the "Context" for the "Character". If a piece of information is not available in the context, leave the corresponding value as an empty string. Provide only the JSON object as your response, without any additional explanation or extra fields.

Context: {context}
Character: {character}

Reply in the JSON format:

{{
    "name": "",
    "hairColor": "",
    "house": "",
    "wandSizeInInches": "",
    "petType": ""
}}

Provide the JSON directly without surrounding backticks. Only provide information in JSON.
"""

llm = OllamaLLM(model="llama3.1:8b")
template = PromptTemplate.from_template(prompt)
encoding = tiktoken.get_encoding("cl100k_base")

def read_txt(file_path):
    from langchain_community.document_loaders import PyMuPDFLoader
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    return " ".join([doc.page_content for doc in docs])

def limit_tokens(text: str, max_tokens: int) -> str:
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        return encoding.decode(tokens[:max_tokens])
    return text

def run_llm_w_rag(books: List[str], query: str, max_tokens: int):
    book_text = [read_txt(book) for book in books]
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    chunks = [chunk for text in book_text for chunk in splitter.split_text(text)]
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vector_store = FAISS.from_texts(chunks, embeddings)
    retriever = vector_store.as_retriever()

    def retrieve_and_limit(query):
        retrieved_docs = vector_store.similarity_search(query, k=10)
        context = " ".join([doc.page_content for doc in retrieved_docs])
        limited_context = limit_tokens(context, max_tokens)
        print("Input tokens (with RAG):", len(encoding.encode(limited_context)))
        return limited_context
    
    
    rag_chain = (
    {"context": retrieve_and_limit, "character": RunnablePassthrough()}
    | template
    | llm
    | JsonOutputParser()
    )

    return rag_chain.invoke(query)




def run_llm_wo_rag(books: List[str], query: str,  max_tokens: int):
    book_text = [read_txt(book) for book in books]
    book_complete = " ".join(book_text)
    # Limit context tokens
    limited_context = limit_tokens(book_complete, max_tokens)

    chain = (
    {"context": lambda _: limited_context, "character": RunnablePassthrough()}
    | template
    | llm
    | JsonOutputParser()
    )

    # Print number of input tokens
    print("Input tokens (without RAG):", len(encoding.encode(limited_context)))

    return chain.invoke(query)

def score_source(data: dict):
    source = {
      "name": "Harry James Potter",
      "hairColor": "Black",
      "house": "Gryffindor",
      "wandSizeInInches": "11 inches",
      "petType": "Owl"
    }

    score = 0
    for key in data.keys():
        score += process.fuzz.partial_ratio(str(source[key]), str(data[key]))

    return score /5

# Example usage
query = "Harry Potter"

for tokens in [128000]:
    print(colored(f"Running with {tokens} tokens", "red", "on_white"))
    # w_rag = run_llm_w_rag(['books/hp1.pdf', 'books/hp2.pdf'], query, tokens)
    # print(colored(f"With RAG: {w_rag}", "yellow"))
    # print(colored(f"With RAG - Score against Truth: {score_source(w_rag)}", "green"))
    wo_rag = run_llm_wo_rag(['books/hp1.pdf', 'books/hp2.pdf'], query, tokens)
    print(colored(f"Without RAG: {wo_rag}", "yellow"))
    print(colored(f"Without RAG - Score against Truth: {score_source(wo_rag)}", "cyan"))