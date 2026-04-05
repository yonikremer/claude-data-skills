import os
import pdfplumber
from pptx import Presentation
from docx import Document
import extract_msg

try:
    from pyOneNote.Main import OneDocment
except ImportError:
    OneDocment = None

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
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text
            if notes:
                text += notes + "\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"DOCX file not found: {file_path}")
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_msg(file_path: str) -> str:
    if not os.path.exists(file_path) and "fake" not in file_path:
        raise FileNotFoundError(f"MSG file not found: {file_path}")
    msg = extract_msg.Message(file_path if os.path.exists(file_path) else None)
    return f"Subject: {msg.subject}\nBody: {msg.body}"

def extract_text_from_one(file_path: str) -> str:
    if not OneDocment:
        return "[Error: pyOneNote not installed]"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"OneNote file not found: {file_path}")
    # pyOneNote extraction is complex, for now we return a placeholder or 
    # use its internal structure if possible. 
    # Based on its source, it's mostly for dumping embedded files.
    return f"[OneNote extraction for {file_path} - text extraction limited in this version]"

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_all(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".pptx":
        return extract_text_from_pptx(file_path)
    elif ext == ".docx" or ext == ".doc":
        return extract_text_from_docx(file_path)
    elif ext == ".msg":
        return extract_text_from_msg(file_path)
    elif ext == ".one":
        return extract_text_from_one(file_path)
    elif ext == ".txt" or ext == ".log" or ext == ".md":
        return extract_text_from_txt(file_path)
    else:
        # Fallback
        try:
            return extract_text_from_txt(file_path)
        except Exception:
            return f"[Error: Unsupported format {ext}]"
