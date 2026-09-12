import os
import re
from pypdf import PdfReader
from logging_utils.log import setup_logger

logger = setup_logger("pdf_cleaner.log")

def extract_cleaned_pdf(pdf_path: str):
    if not os.path.exists(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        return []
        
    reader = PdfReader(pdf_path)
    pages = []
    
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                # 1. Remove Page Numbers
                text = re.sub(r'(?i)page\s*\d+(\s*of\s*\d+)?', '', text)
                
                # 2. Normalize whitespace
                text = re.sub(r'[ \t]+', ' ', text)
                text = re.sub(r'\n\s*\n', '\n', text)
        
                pages.append(text.strip())
        except Exception as e:
            logger.error(f"Error reading page {i}: {e}")
            
    logger.success(f"Successfully extracted and cleaned {len(pages)} pages.")
    return pages

if __name__ == "__main__":
    # Test run
    test_pages = extract_cleaned_pdf("/mnt/c/Users/Gopi/Desktop/python_devops/Data_Scientist_Role.pdf")