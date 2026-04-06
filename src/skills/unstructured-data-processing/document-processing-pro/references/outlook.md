# Outlook (.msg, .pst) Reference

## extract-msg (Python)

Library for reading Microsoft Outlook MSG files.

### Basic Usage

```python
import extract_msg

# Open MSG file
msg = extract_msg.Message("test.msg")

# Core properties
sender = msg.sender
recipient = msg.to
subject = msg.subject
date = msg.date
body = msg.body
html_body = msg.htmlBody # if available

# Save message to disk (as a folder containing text and attachments)
msg.save()

# List attachments
for attachment in msg.attachments:
    print(f"Attachment: {attachment.getFilename()}")
    attachment.save()
```

### Advanced: Handling RTF/HTML Bodies

Outlook emails often store the body in multiple formats. Always check for HTML first if formatting is required, falling back to RTF or plain text.

```python
if msg.htmlBody:
    process_html(msg.htmlBody)
elif msg.rtfBody:
    process_rtf(msg.rtfBody)
else:
    process_text(msg.body)
```

## libpst / readpst (Linux/C)

`libpst` is the standard library for reading PST (Outlook Personal Folders) files.

### Command Line (readpst)

```bash
# Extract all emails from a PST file into a folder structure
readpst -o output_dir archive.pst

# Extract as individual MSG files (requires additional tools or specific flags)
readpst -M -o output_dir archive.pst
```

### Python Bindings (libpypst)

If available, `libpypst` provides a more direct way to iterate through PST folders.

---

## Common Pitfalls

- **Embedded Messages**: An MSG file can contain another MSG file as an attachment. Use `msg.attachments` recursively.
- **MIME Types**: MSG files are NOT MIME-compliant. They are OLE documents.
- **Large PSTs**: PST files can be many gigabytes. Use streaming or folder-by-folder processing to avoid OOM.
