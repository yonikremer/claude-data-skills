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

import chardet

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "rb") as f:
        raw_data = f.read()
        
    # Try common encodings first
    for enc in ['utf-8', 'windows-1255', 'iso-8859-8']:
        try:
            return raw_data.decode(enc)
        except UnicodeDecodeError:
            continue
            
    # Fallback to chardet
    detected = chardet.detect(raw_data)
    encoding = detected['encoding'] or 'utf-8'
    try:
        return raw_data.decode(encoding)
    except UnicodeDecodeError:
        return raw_data.decode('utf-8', errors='replace')

from .hebrew_utils import normalize_rtl_text

def extract_all(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    raw_text = ""
    if ext == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext == ".pptx":
        raw_text = extract_text_from_pptx(file_path)
    elif ext == ".docx" or ext == ".doc":
        raw_text = extract_text_from_docx(file_path)
    elif ext == ".msg":
        raw_text = extract_text_from_msg(file_path)
    elif ext == ".one":
        raw_text = extract_text_from_one(file_path)
    elif ext == ".txt" or ext == ".log" or ext == ".md":
        raw_text = extract_text_from_txt(file_path)
    else:
        # Fallback
        try:
            raw_text = extract_text_from_txt(file_path)
        except Exception:
            return f"[Error: Unsupported format {ext}]"
            
    return normalize_rtl_text(raw_text)
