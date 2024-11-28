import fitz  # PyMuPDF
from transformers import pipeline, Pipeline
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from typing import List, Optional
import re
import os

def mask_additional_pii(text):
    # academmic/professional titles
    title_pattern = re.compile(r'\b(Dr|Professor|Assistant Professor|Associate Professor|Director|Manager)\.?\s[A-Z][a-z]*\s?[A-Z]?[a-z]*\b', re.IGNORECASE)
    
    # Handle university names
    university_pattern = re.compile(r'\b[A-Z][a-z]*(\sCollege|\sUniversity|\sInstitute)\b', re.IGNORECASE)
    
    # mask urls
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    # Replace patterns
    text = title_pattern.sub('[Title]', text)
    text = university_pattern.sub('[Institution]', text)
    text = url_pattern.sub('[URL]', text)
    
    location_pattern = re.compile(r'\b[A-Z][a-z]+,\s[A-Z][a-z]+\b', re.IGNORECASE)
    text = location_pattern.sub('[Location]', text)
    
    return text

def load_model(model_tag: str, use_gpu: bool = False) -> Optional[Pipeline]:
    device = 0 if use_gpu else -1
    try:
        model = pipeline("token-classification", model=model_tag, tokenizer=model_tag, device=device)
        return model
    except Exception as e:
        print(f"Error loading Model: \n\n{e}")
        return None

def create_entity_map(model_output: List[dict], text: str) -> dict:
    entity_map = {}
    for token in model_output:
        start = token["start"]
        end = token["end"]
        entity = text[start: end]
        entity_map[entity] = token["entity_group"]
    return entity_map

def replace_entities(text: str, entity_map: dict) -> str:
    for word in entity_map:
        if word in text:
            text = text.replace(word, f"[{entity_map[word]}]")
    return text

def mask_pii(input_sentence: str, anonymizer: Pipeline) -> Optional[str]:
    output = anonymizer(input_sentence, aggregation_strategy="simple")
    if isinstance(output, list):
        entity_map = create_entity_map(output, input_sentence)
        masked_text = replace_entities(input_sentence, entity_map)
        # Enhanced PII masking with additional post-processing
        return mask_additional_pii(masked_text)
        # return masked_text
    else:
        print("Output is not in the expected format")
        return None

def add_text_to_canvas(c, text, max_width=7.5*72, max_height=10*72):
    from reportlab.lib.utils import simpleSplit
    text_object = c.beginText(72, max_height-72)
    text_object.setFont("Times-Roman", 12)
    # Split text into lines and pages
    lines = simpleSplit(text, "Times-Roman", 12, max_width)
    for line in lines:
        if text_object.getY() - 12 < 72:  # margin test
            c.drawText(text_object)
            c.showPage()
            text_object = c.beginText(72, max_height-72)
            text_object.setFont("Times-Roman", 12)
        text_object.textLine(line)
    c.drawText(text_object)

def process_pdf_and_create_masked_pdf(input_pdf_path: str, output_pdf_path: str, anonymizer_model: Pipeline, anonymizer_model2: Pipeline):
    doc = fitz.open(input_pdf_path)
    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    # Process and add masked text for each page in the LoR
    for i, page in enumerate(doc):
        text = page.get_text("text")
        # text = text.lower()
        # with(open(f"text_{i}.txt", "w")) as f:
        #     f.write(text)
        masked_text = mask_pii(text, anonymizer_model)
        # masked_text2 = mask_pii(masked_text, anonymizer_model2)
        if masked_text:
            add_text_to_canvas(c, masked_text)

    c.save()

# Load the model
# anonymizer_model2 = load_model("Isotonic/deberta-v3-base_finetuned_ai4privacy_v2")
# anonymizer_model = load_model("Isotonic/distilbert_finetuned_ai4privacy_v2")
# anonymizer_model = load_model("Isotonic/mdeberta-v3-base_finetuned_ai4privacy_v2")

def process_folder(input_folder: str, output_folder: str, anonymizer_model: Pipeline):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # List all PDF files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, filename)
            print(f"Processing {filename}...")
            process_pdf_and_create_masked_pdf(input_pdf_path, output_pdf_path, anonymizer_model, anonymizer_model)
            print(f"Anonymized version of {filename} saved.")
    print("All documents processed.")


anonymizer_model = load_model("Isotonic/distilbert_finetuned_ai4privacy_v2")

if anonymizer_model:
    input_folder = 'sopdocs'  # Folder containing the letters
    output_folder = 'masked_docs'  # Folder to store the masked documents
    process_folder(input_folder, output_folder, anonymizer_model)
