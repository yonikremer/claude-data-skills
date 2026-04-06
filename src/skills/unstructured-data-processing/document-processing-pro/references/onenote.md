# Local OneNote (.one, .onetoc2) Reference

Parsing local Microsoft OneNote files requires specialized tools because the format is a proprietary binary OLE container.

## Recommended Tools

### 1. MarkItDown (Microsoft Official)

Best for high-fidelity conversion of OneNote sections to Markdown. It handles text extraction elegantly and is optimized for LLM consumption.

- **Installation**: `pip install markitdown`
- **Usage**:
  ```python
  from markitdown import MarkItDown
  md = MarkItDown()
  result = md.convert("meeting_notes.one")
  print(result.text_content)
  ```

### 2. onenote2xml

A robust parser that can extract the full structure of `.one` (sections) and `.onetoc2` (table of contents) files into XML or JSON.

- **GitHub**: `alegrigoriev/onenote2xml`
- **Capabilities**: Preserves page hierarchy, author metadata, and revision history.
- **Example**: `python 1note2json.py my_notes.one > notes.json`

### 3. one-extract

Specialized for extracting embedded attachments and media from OneNote files.

- **Installation**: `pip install one-extract`
- **CLI Usage**: `one-extract my_notes.one` (Extracts files to a local directory).

### 4. pyOneNote

Forensic-focused tool for analyzing OneNote headers and extracting embedded objects.

- **GitHub**: `DissectMalware/pyOneNote`

---

## File Types

- **.one**: Represents a single **Section** in a notebook. Contains the actual page content, text, and images.
- **.onetoc2**: Represents the **Table of Contents** for a notebook. It defines the order of sections and section groups but contains **no page content**.

---

## Common Pitfalls

- **Proprietary Binary Format**: Never use `open(file, 'r')` or regex to parse `.one` files. They are non-textual OLE containers.
- **Sync States**: If a notebook is currently being synced by the OneNote desktop app, the `.one` file might be locked or in a transient state.
- **Missing Images**: Some images might be stored as references to other cache files rather than embedded directly.
- **Ink Data**: Handwritten notes (ink) are notoriously difficult to extract as text from local files without using OCR on a rendered version.
