---
name: data-format-detection
description: Identifies the format and encoding of unknown binary files or raw bytes. Use for deep forensic inspection of unlabelled data using magic bytes, ffprobe, and bitwise similarity.
---
# Data Format Detection (Forensic Grade)

This skill provides a professional framework for identifying unknown data formats and character encodings.

## 1. Magic Byte Identification (MANDATORY TOOLS)

NEVER rely on manual dictionaries. Use industry-standard libraries that wrap the `libmagic` database.

### python-magic (Primary)
```python
import magic

# Detect MIME type
mime = magic.from_file('unknown_blob', mime=True)
# Detect human description
desc = magic.from_file('unknown_blob')
print(f"MIME: {mime} ({desc})")
```

### filetype (Zero-dependency fallback)
Use for common file types (images, video, archives) if `libmagic` is unavailable.
```python
import filetype
kind = filetype.guess('unknown_blob')
if kind:
    print(f"Extension: {kind.extension}, MIME: {kind.mime}")
```

## 2. Media Discovery with FFprobe
If a file lacks headers but is suspected to be a media stream (raw PCM, H.264, etc.), use FFprobe.

```bash
# Force probe all streams
ffprobe -v error -show_format -show_streams unknown_file

# Check for specific metadata
ffprobe -i unknown_file -show_entries format=format_name,duration -of default=noprint_wrappers=1
```

## 3. Encoding Detection (MANDATORY)

For text-like data, use `charset-normalizer` (the modern successor to `chardet`).

```python
from charset_normalizer import from_path

results = from_path('unknown.txt')
best_guess = results.best()

if best_guess:
    print(f"Encoding: {best_guess.encoding} (Confidence: {best_guess.ratio})")
    # Open with the detected encoding
    content = str(best_guess)
```

## 4. Bitwise Periodic Structure (The "Frame Size" Trick)

For raw telemetry, sensor data, or unaligned binary streams, use bit-level self-similarity to find the record size.

**Logic**: Convert the file to a bitstream and search for the bit-period (1 to file size) where adjacent bit-frames are most similar (lowest XOR difference).

```python
# Use the optimized bitwise detector:
# python skills/data-format-detection/scripts/periodic_structure_detector.py <file>
```

## 5. Entropy & Forensic Analysis

- **Entropy**: High entropy (>7.5 bits/byte) indicates compression or encryption. Low entropy (<4.0) indicates highly structured/sparse data.
- **CyberChef Patterns**:
  - **Base64 + Gzip**: Web/API payloads.
  - **XOR Brute Force**: Simple obfuscation.
  - **Bit Flip**: Corrupted streams.
- **Strings**: Always check for human-readable content.
  ```bash
  strings -n 6 unknown_file | head -n 20
  ```

## 6. Compression Sniffing
If magic bytes are missing, try transparent decompression:
```python
import gzip, zlib, bz2, lzma

def sniff_compression(data):
    # Try common headers
    if data.startswith(b'\x1f\x8b'): return "gzip"
    if data.startswith(b'BZh'): return "bzip2"
    # Try raw zlib
    try:
        zlib.decompress(data)
        return "zlib (raw)"
    except:
        pass
    return None
```
