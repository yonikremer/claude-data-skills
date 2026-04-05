import os
from typing import List

# Lazy imports for heavy libraries
_easyocr = None
_pdf2image = None

def _get_easyocr():
    global _easyocr
    if _easyocr is None:
        import easyocr
        _easyocr = easyocr.Reader(['he', 'en'])
    return _easyocr

def _get_pdf2image():
    global _pdf2image
    if _pdf2image is None:
        import pdf2image
        _pdf2image = pdf2image
    return _pdf2image

def extract_text_via_ocr(file_path: str) -> str:
    """
    Performs pixel-based OCR on a PDF file.
    Requires 'poppler' system dependency.
    """
    try:
        p2i = _get_pdf2image()
        reader = _get_easyocr()
        
        # Convert PDF pages to images
        # We limit to first 50 pages for large files to prevent OOM
        pages = p2i.convert_from_path(file_path, first_page=1, last_page=50)
        
        full_text = []
        for i, page in enumerate(pages):
            # Convert PIL image to bytes or temporary file for easyocr
            # easyocr can take PIL images directly
            import numpy as np
            results = reader.readtext(np.array(page), detail=0)
            full_text.append(" ".join(results))
            
        return "\n".join(full_text)
    except Exception as e:
        return f"[OCR Error: {str(e)} - Ensure poppler and easyocr are installed correctly]"
