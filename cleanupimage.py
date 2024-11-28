from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re

def pdf_to_images(pdf_path):
    # Convert PDF to images (one image per page)
    images = convert_from_path(pdf_path)
    return images

def ocr_on_image(image):
    # Use pytesseract to extract text from an image
    text = pytesseract.image_to_string(image)
    return text

def clean_extracted_text(text):
    # Clean the text using the same method as before
    cleaned_text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a space
    cleaned_text = re.sub(r'(\w)-\s+(\w)', r'\1\2', cleaned_text)  # Fix hyphenated line breaks
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  # Replace multiple spaces with a single space
    cleaned_text = cleaned_text.replace('\x0c', '')  # Remove control characters
    cleaned_text = cleaned_text.strip()  # Remove leading and trailing whitespace

    return cleaned_text

def return_cleaned_text(pdf_path):
    # Convert PDF to images
    images = pdf_to_images(pdf_path)

    # Perform OCR on each image and aggregate the results
    extracted_text = ''
    for image in images:
        extracted_text += ocr_on_image(image) + '\n'

    # Clean the extracted text
    cleaned_text = clean_extracted_text(extracted_text)
    # print(cleaned_text)
    # print(" --------------------\n\n")

    return cleaned_text

# pdf_path = 'parsedProfiles/supasec/academic_information.pdf'
# pdf_path2 = 'parsedProfiles/supasec/student_information.pdf'
# cleaned_text = return_cleaned_text(pdf_path)
# cleaned_text2 = return_cleaned_text(pdf_path2)