import ocrmypdf
from ocrmypdf.exceptions import PriorOcrFoundError
import fitz  # PyMuPDF
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

def replace_pii_in_text(text):
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    
    # Analyze the text to find PII
    analyzer_results = analyzer.analyze(text=text, language='en')
    
    # Anonymize the text
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
    
    return anonymized_text.text

def process_pdf(input_pdf, output_pdf):
    # First, perform OCR on the input PDF
    try:
        ocrmypdf.ocr(input_pdf, output_pdf, skip_text=True)
    except PriorOcrFoundError as e:
        print(f"OCR process skipped for '{input_pdf}' as it contains pre-existing text. Error: {e}")
    
    # Now, open the OCR'd PDF and redact PII
    pdf_document = fitz.open(output_pdf)
    
    for page in pdf_document:
        text = page.get_text()
        redacted_text = replace_pii_in_text(text)
        
        # Clear the page and insert the redacted text
        page.clear_text()
        page.insert_text((0, 0), redacted_text)
    
    pdf_document.save(output_pdf)
    pdf_document.close()

# Usage
input_pdf = "rawProfiles/image.pdf"
output_pdf = "rawProfiles/imageconverted.pdf"
process_pdf(input_pdf, output_pdf)

print(f"Processed PDF saved to {output_pdf}")