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

def process_pdf(input_pdf):
    pdf_document = fitz.open(input_pdf)
    full_text = ""
    
    for page in pdf_document:
        text = page.get_text()

        full_text += text 
    
    pdf_document.close()
    return full_text

# Usage
input_pdf = "processedDocs/imageconverted.pdf"
print(f"Processing {input_pdf}")
redacted_text = process_pdf(input_pdf)
print(redacted_text)

# Usage
# input_pdf = "rawProfiles/SreeHariKarri.pdf"
# output_pdf = "rawProfiles/replaced_output.pdf"
# process_pdf(input_pdf, output_pdf)