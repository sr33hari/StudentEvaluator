import spacy
import fitz  # PyMuPDF

def redact_pii(input_pdf, output_pdf):
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Open the PDF
    doc = fitz.open(input_pdf)
    
    for page in doc:
        # Extract text from the page
        text = page.get_text()
        
        # Process the text with spaCy
        processed_text = nlp(text)
        
        # Identify PII entities
        pii_entities = [ent.text for ent in processed_text.ents if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "MONEY"]]
        
        # Redact PII entities
        for entity in pii_entities:
            areas = page.search_for(entity)
            for area in areas:
                page.add_redact_annot(area, fill=(0, 0, 0))
        
        # Apply the redactions
        page.apply_redactions()
    
    # Save the redacted PDF
    doc.save(output_pdf, garbage=4, deflate=True, clean=True)
    doc.close()

# Usage
input_pdf = "rawProfiles/SreeHariKarri.pdf"
output_pdf = "rawProfiles/redacted_output.pdf"
redact_pii(input_pdf, output_pdf)