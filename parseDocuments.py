import json
from pathlib import Path
import ollama
import pdfplumber
import re
import os
import fitz  # PyMuPDF
import ocrmypdf
from ocrmypdf.exceptions import PriorOcrFoundError
from PyPDF2 import PdfWriter, PdfReader
from termcolor import colored
import cleanupimage
import templates

# Regex patterns for the required sections
patterns = {
    "supporting_information": re.compile(r"SUPPORTING INFORMATION", re.IGNORECASE),
    "statement_of_purpose": re.compile(r"STATEMENT OF PURPOSE", re.IGNORECASE),
    "evaluation": re.compile(r"EVALUATION", re.IGNORECASE),
    "letter_of_recommendation": re.compile(r"LETTER OF RECOMMENDATION", re.IGNORECASE)
}

class FilenameConstants:
    STUDENT_INFORMATION = "student_information"
    ACADEMIC_INFORMATION = "academic_information"
    SUPPORTING_INFORMATION = "supporting_information"
    STATEMENT_OF_PURPOSE = "statement_of_purpose"
    EVALUATIONS_AND_LORS = "evaluations_and_lors"

def clean_duplicated_characters(text):
    # """Remove duplicated characters from the string."""
    # cleaned_text = ""
    # skip_next = False
    # for i in range(len(text) - 1):
    #     if skip_next:
    #         skip_next = False
    #         continue
    #     if text[i] == text[i + 1]:
    #         cleaned_text += text[i]
    #         skip_next = True
    #     else:
    #         cleaned_text += text[i]
    #         skip_next = False
    # if not skip_next:
    #     cleaned_text += text[-1]
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from each page of the PDF and clean it."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_by_page = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    cleaned_page_text = clean_duplicated_characters(page_text)
                    text_by_page.append(cleaned_page_text)
                else:
                    text_by_page.append("")  # Add an empty string for pages with no text
    except Exception:
        text_by_page = ocr_extract_text_from_pdf(pdf_path)
    return text_by_page

def ocr_extract_text_from_pdf(pdf_path):
    """Extract text from each page of the PDF using OCR and clean it."""
    ocr_pdf_path = "temp_ocr.pdf"
    try:
        ocrmypdf.ocr(pdf_path, ocr_pdf_path, skip_text=True)
    except PriorOcrFoundError:
        ocr_pdf_path = pdf_path  # If the PDF already contains text, use the original

    text_by_page = []
    with fitz.open(ocr_pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text:
                cleaned_text = clean_duplicated_characters(text)
                text_by_page.append(cleaned_text)
            else:
                text_by_page.append("")
    if ocr_pdf_path == "temp_ocr.pdf":
        os.remove(ocr_pdf_path)
    return text_by_page

def split_pdf_by_headings(input_pdf_path, output_dir):
    """Split the PDF into sections based on headings."""
    # Extract text from the PDF and get text by page
    text_by_page = extract_text_from_pdf(input_pdf_path)

    num_lors = 0

    # Open the input PDF file
    with open(input_pdf_path, 'rb') as infile:
        reader = PdfReader(infile)
        num_pages = len(reader.pages)

        # print("Writing the first page into a new PDF file\n")
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        with open(os.path.join(output_dir, "student_information.pdf"), 'wb') as outfile:
            writer.write(outfile)
        
        # print("Writing the second page into a new PDF file\n")
        writer = PdfWriter()
        writer.add_page(reader.pages[1])
        with open(os.path.join(output_dir, "academic_information.pdf"), 'wb') as outfile:
            writer.write(outfile)
        

        # Initialize variables
        sections = {
            "supporting_information": [],
            "statement_of_purpose": [],
            "evaluations_and_lors": []
        }

        current_section = None

        # Iterate through all the pages and classify them based on headings
        for i in range(num_pages):
            text = text_by_page[i] if i < len(text_by_page) else ""

            # print(f"Processing page {i + 1} of {num_pages}")
            # print(f"Page text: {text}")

            if patterns["supporting_information"].search(text):
                print("\n\n\nFound supporting information\n\n\n")
                current_section = "supporting_information"
            elif patterns["statement_of_purpose"].search(text):
                print("\n\n\nFound statement of purpose\n\n\n")
                current_section = "statement_of_purpose"
            elif patterns["evaluation"].search(text):
                print("\n\n\nFound evaluation\n\n\n")
                current_section = "evaluations_and_lors"
            elif patterns["letter_of_recommendation"].search(text):
                print("\n\n\nFound letter of recommendation\n\n\n")
                current_section = "evaluations_and_lors"
                num_lors += 1

            if current_section:
                sections[current_section].append(i)

        # Function to write pages to a PDF file

        def write_pages_to_pdf(pages, output_path):
            writer = PdfWriter()
            for page_num in pages:
                writer.add_page(reader.pages[page_num])
            with open(output_path, 'wb') as outfile:
                writer.write(outfile)

        # Write supporting information PDF
        if sections["supporting_information"]:
            write_pages_to_pdf(sections["supporting_information"], os.path.join(output_dir, "supporting_information.pdf"))

        # Write statement of purpose PDF
        if sections["statement_of_purpose"]:
            write_pages_to_pdf(sections["statement_of_purpose"], os.path.join(output_dir, "statement_of_purpose.pdf"))

        # Write evaluations and letters of recommendation PDF
        if sections["evaluations_and_lors"]:
            write_pages_to_pdf(sections["evaluations_and_lors"], os.path.join(output_dir, "evaluations_and_lors.pdf"))
    
    return num_lors

def process_directory(input_dir, output_dir):
    """Process all PDFs in the input directory and split them based on headings."""
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    directories = []
    num_lors = 0

    # check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return directories
    
    # Iterate over all PDF files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            input_pdf_path = os.path.join(input_dir, filename)
            profile_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])
            
            # Create sub-directory for each PDF
            os.makedirs(profile_output_dir, exist_ok=True)
            directories.append(profile_output_dir)

            
            # Split the PDF by headings
            num_lors = split_pdf_by_headings(input_pdf_path, profile_output_dir)
    
    return directories, num_lors

def process_single_profile(input_pdf_path, output_dir):
    """Process single Profile PDF and split them based on headings."""
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    profile_output_dir = os.path.join(output_dir, Path(input_pdf_path).stem)
    
    # Create sub-directory for each PDF
    os.makedirs(profile_output_dir, exist_ok=True)
    
    num_lors = split_pdf_by_headings(input_pdf_path, profile_output_dir)
    return profile_output_dir


def get_text_content(directory):
    """Get the text content from all PDFs in the directory. Return a dictionary with filenames as keys and their entire text content as values."""
    text_content = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            if filename == "student_information.pdf" or filename == "academic_information.pdf":
                parsedText = cleanupimage.return_cleaned_text(pdf_path)
            else:
                parsedText = cleanupimage.return_cleaned_text(pdf_path)
                # parsedText = extract_text_from_pdf(pdf_path)
            # text_content = "\n--------\n".join(text_by_page)
            text_content[filename] = parsedText
    return text_content

def get_student_name_and_email(directory):
    filename = directory + "/"+f"{FilenameConstants.STUDENT_INFORMATION}.pdf"
    print(f"Processing file {filename}")
    student_name = ""
    student_email = ""
    # student_information_filename = f"{FilenameConstants.STUDENT_INFORMATION}.pdf"
    # if filename == student_information_filename:
    #     #Extract Student Name and Email
    text_content = get_text_content(directory)
    #print the keys of text_content
    print(text_content.keys())

    prompt = templates.TEMPLATES.get(f"{FilenameConstants.STUDENT_INFORMATION}.pdf")
    # student_info_file = f"{Path(filename).stem}.pdf"
    content_with_prompt = text_content[f"{FilenameConstants.STUDENT_INFORMATION}.pdf"] + '\n' + prompt
    response = ollama.chat(model='llama3.1:8b', messages=[
        {
            'role': 'user',
            'content': content_with_prompt,
        },
    ], options={"temperature": 0.2})
    print(colored(f"Response for file {filename}: {response['message']['content']} ", "green"))
    student_name = json.loads(response['message']['content']).get('Name', 'N/A')
    student_email = json.loads(response['message']['content']).get('Email', 'N/A')

    return student_name, student_email

def get_filenames(directory):
    """Get all the filenames in the directory."""
    filenames = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            filenames.append(filename)
    return filenames

def identify_number_of_lors(input_pdf_path):
    """Identify the number of letters of recommendation from the text content."""
    num_lors = 0

    with open(input_pdf_path, 'rb') as infile:
        reader = PdfReader(infile)
        num_pages = len(reader.pages)

        text_by_page = extract_text_from_pdf(input_pdf_path)
        for i in range(num_pages):
            text = text_by_page[i] if i < len(text_by_page) else ""
            if patterns["letter_of_recommendation"].search(text):
                print(colored("Found letter of recommendation", "red", "on_white"))
                num_lors += 1

    return num_lors

if __name__ =="__main__":
    # Define the input directory and the output directory
    input_dir = 'rawProfiles'
    output_dir = 'parsedProfiles'

    # Process the directory
    dir_list = process_directory(input_dir, output_dir)