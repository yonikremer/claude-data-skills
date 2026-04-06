---
name: document-processing-pro
description: Use for creating, reading, and manipulating Office documents (DOCX, XLSX, PPTX, MSG, PST, ONE) and PDFs. High-fidelity extraction, professional formatting, and automated report generation. CRITICAL: For large files or image-heavy docs, run `get-available-resources` first.
---

# Document Processing Pro (Consolidated)

Unified guide for professional document manipulation across PDF and Microsoft Office formats.

## ⚠️ Mandatory Pre-flight: Resource Check

Large documents (especially PDFs with high-res images or 100+ page Word docs) can consume significant RAM during
parsing.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Strategy**:
    - **Text-only**: Standard libraries (`python-docx`, `pypdf`) are fine.
    - **Image-heavy/OCR**: Ensure 4GB+ RAM available before running `pytesseract` or `pdf2image`.
    - **Massive XLSX**: Use `polars` or `openpyxl` with `read_only=True`.

---

## 1. Word Documents (.docx)

Use for reports, memos, and automated document generation.

### Core Idioms

- **Creation**: Use `docx-js` (Node.js) for high-fidelity formatting. **Always set page size explicitly.**
- **Editing**: Follow the 3-step XML workflow: **Unpack → Edit XML → Pack**.
- **Tracked Changes**: Use `<w:ins>` and `<w:del>` tags in the XML.

```javascript
// Creating with docx-js
const { Document, Paragraph, TextRun } = require('docx');
const doc = new Document({
    sections: [{
        properties: { page: { size: { width: 12240, height: 15840 } } }, // US Letter
        children: [new Paragraph({ children: [new TextRun("Hello World")] })]
    }]
});
```

---

## 2. PDF Manipulation

Use for extraction, merging, and filling forms.

### Core Tools

- **Extraction**: Use `pdfplumber` for tables and layout-aware text.
- **Manipulation**: Use `pypdf` for merging, splitting, and rotating.
- **Creation**: Use `reportlab` for generating PDFs from scratch.

```python
import pdfplumber
from pypdf import PdfWriter

# Extract Table
with pdfplumber.open("report.pdf") as pdf:
    table = pdf.pages[0].extract_table()

# Merge PDFs
writer = PdfWriter()
for path in ["file1.pdf", "file2.pdf"]:
    writer.append(path)
writer.write("merged.pdf")
```

---

## 3. Spreadsheets (.xlsx, .csv)

Use for data entry, formatting, and complex workbooks.

### Core Tools

- **Small/Medium**: Use `pandas` or `openpyxl`.
- **High Performance**: Use `polars` for CSV/Parquet.
- **Formatting**: Use `xlsxwriter` for charts and conditional formatting.

```python
import pandas as pd

# Load specific sheet
df = pd.read_excel("data.xlsx", sheet_name="Financials")

# Write with formatting
writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1")
workbook = writer.book
# Add chart/formatting here...
writer.close()
```

---

## 4. Presentations (.pptx)

Use for automated slide generation and template population.

### Core Tool: `python-pptx`

- **Idiom**: Always work with `SlideLayouts` from your template.

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0]) # Title Slide
slide.shapes.title.text = "Automated Report"
prs.save("presentation.pptx")
```

---

## 5. Outlook Emails (.msg, .pst)

Use for parsing emails, attachments, and mailbox archives.

### Core Tools

- **Single Emails (.msg)**: Use `extract-msg` for parsing headers, body, and attachments from standalone MSG files.
- **Mailbox Archives (.pst)**: Use `libpst` (via command line or Python bindings) to extract entire folders of emails and attachments.

```python
import extract_msg

msg = extract_msg.Message("email.msg")
msg_sender = msg.sender
msg_date = msg.date
msg_subj = msg.subject
msg_body = msg.body

# Save attachments
for attachment in msg.attachments:
    attachment.save(customPath="attachments_dir")
```

---

## 6. OneNote Notebooks (.one, .onetoc2)

Use for parsing and extracting notes, sections, and attachments from local OneNote files.

### Core Tools

- **Text Extraction**: Use `MarkItDown` (Microsoft's official converter) to convert `.one` files into clean Markdown.
- **Structured Extraction**: Use `onenote2xml` for detailed XML/JSON representations of notebook hierarchy and page history.
- **Attachments**: Use `one-extract` for retrieving embedded files and media.

```python
from markitdown import MarkItDown

# High-fidelity conversion to Markdown
md = MarkItDown()
result = md.convert("notebook_section.one")
print(result.text_content)
```

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **DOCX**: Never use `\n` in `docx-js`; use separate `Paragraph` objects.
2. **PDF**: Never use Unicode subscripts (₀₁₂) in `reportlab`; use `<sub>` tags.
3. **XLSX**: Don't load 100MB+ Excel files into `pandas` without checking RAM; use `polars`.
4. **MSG**: Email bodies can be in RTF, HTML, or plain text. Don't assume plain text exists without falling back.
5. **ONE**: Local `.one` files are binary OLE containers. Parsing requires specialized tools; never attempt manual regex/string extraction.
6. **ONE TOC**: `.onetoc2` files contain notebook structure (folders/sections) but no actual page content.
7. **General**: Never catch `ImportError` silently. Let the agent see if a library is missing.

## References

- `skills/unstructured-data-processing/document-processing-pro/scripts/docx/` — XML patterns and docx-js API.
- `skills/unstructured-data-processing/document-processing-pro/references/pdf.md` — OCR and advanced manipulation.
- `skills/unstructured-data-processing/document-processing-pro/references/xlsx/` — XlsxWriter and formatting.
- `skills/unstructured-data-processing/document-processing-pro/references/outlook.md` — extract-msg and libpst usage.
- `skills/unstructured-data-processing/document-processing-pro/references/onenote.md` — MarkItDown and onenote2xml for local parsing.
- `skills/unstructured-data-processing/document-processing-pro/scripts/outlook/` — Email extraction scripts.
- `skills/unstructured-data-processing/document-processing-pro/scripts/onenote/` — Local .one parsing examples.
