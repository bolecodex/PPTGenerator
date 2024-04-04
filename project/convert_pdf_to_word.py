from PyPDF2 import PdfReader
from docx import Document

def convert_pdf_to_word(pdf_file_path, word_file_path):
    # Create a PDF reader
    pdf_reader = PdfReader(pdf_file_path)

    # Create a Word document
    doc = Document()

    # Extract text from each page of the PDF and add it to the Word document
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:  # Check if text is not None
            doc.add_paragraph(text)

    # Save the Word document
    doc.save(word_file_path)

# Usage
convert_pdf_to_word("Q3_2023_e.pdf", "Q3_2023_e.docx")
