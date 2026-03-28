import pdfplumber
from pptx import Presentation
import os

def extract_text_from_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_pptx(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PPTX file not found: {file_path}")
    
    prs = Presentation(file_path)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
        # Check notes
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text
            if notes:
                text += notes + "\n"
    return text
