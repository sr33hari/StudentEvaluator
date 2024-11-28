import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, output_txt_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Initialize an empty string to store the extracted text
    text = ""
    
    # Iterate through each page in the PDF
    for page in pdf_document:
        # Extract text from the current page
        text += page.get_text()
    
    # Close the PDF document
    pdf_document.close()
    
    # Print the extracted text to the console
    print(text)
    
    # Save the extracted text to a text file
    with open(output_txt_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)
    
    print(f"Text has been saved to {output_txt_path}")

# Usage
pdf_file_path = "rawProfiles/redacted_output.pdf"
output_text_file = "rawProfiles/output.txt"
extract_text_from_pdf(pdf_file_path, output_text_file)