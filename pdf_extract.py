import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import tempfile


st.set_page_config(page_title="PDF Extract", page_icon=":seedling:", menu_items=None)
# Function to convert PDF to text using PyMuPDF
def convert_pdf_to_text(pdf_path):
    text_content = ""
    document = fitz.open(pdf_path)
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text_content += page.get_text()
    return text_content

# Function to convert PDF pages to images and then extract text using OCR
def convert_pdf_to_text_ocr(pdf_path):
    text_content = ""
    pages = convert_from_path(pdf_path)
    for page in pages:
        text_content += pytesseract.image_to_string(page)
    return text_content

# Streamlit application

st.title("PDF to Text Converter")
st.write("Upload a PDF file and extract its text content.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Attempt to extract text using PyMuPDF
    text_content = convert_pdf_to_text(temp_file_path)
    
    # If the text content is empty, use OCR as a fallback
    if not text_content.strip():
        text_content = convert_pdf_to_text_ocr(temp_file_path)

    # Display the extracted text content
    st.text_area("Extracted Text", text_content, height=400)