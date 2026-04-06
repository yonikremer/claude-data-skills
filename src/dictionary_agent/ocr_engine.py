import os
from typing import List
import easyocr
import pdf2image
import numpy as np

# Initialize OCR reader once at module level
_reader = easyocr.Reader(['en'])

def extract_text_via_ocr(file_path: str) -> str:
    """
    Performs pixel-based OCR on a PDF file.
    Requires 'poppler' system dependency.
    """
    try:
        # Convert PDF pages to images
        # We limit to first 50 pages for large files to prevent OOM
        pages = pdf2image.convert_from_path(file_path, first_page=1, last_page=50)
        
        full_text = []
        for i, page in enumerate(pages):
            # Convert PIL image to bytes or temporary file for easyocr
            # easyocr can take PIL images directly
            results = _reader.readtext(np.array(page), detail=0)
            full_text.append(" ".join(results))
            
        return "\n".join(full_text)
    except Exception as e:
        return f"[OCR Error: {str(e)} - Ensure poppler and easyocr are installed correctly]"
