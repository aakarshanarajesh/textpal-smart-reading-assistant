"""
Text Extraction Module
Handles extraction of text from PDF and TXT files
"""

import PyPDF2
import os


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF file
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = ""
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_text_from_txt(file_path):
    """
    Extract text from TXT file
    
    Args:
        file_path (str): Path to the TXT file
        
    Returns:
        str: Content of the TXT file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            text = txt_file.read()
        
        return text.strip()
    except Exception as e:
        return f"Error extracting TXT: {str(e)}"


def extract_text(file_path):
    """
    Determine file type and extract text accordingly
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Extracted text from the file
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    else:
        return "Unsupported file format. Please upload .pdf or .txt files."
