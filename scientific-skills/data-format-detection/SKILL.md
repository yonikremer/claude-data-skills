---
name: data-format-detection
description: Identify the format of unknown raw bytes or files — magic bytes, file signatures, encoding detection, compression detection, and structured format sniffing (CSV, JSON, XML, Parquet, etc.). Use when you receive unknown binary blobs, unlabelled files, or data from legacy systems with no format documentation.
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# Data Format Detection

## Quick Identification Workflow

```python
from pathlib import Path

def identify_file(path: str) -> dict:
    """Run all detectors and return a summary."""
    p = Path(path)
    with open(path, 'rb') as f:
        header = f.read(512)
        f.seek(0, 2)
        size = f.tell()

    return {
        'size_bytes': size,
        'magic':      detect_magic(header),
        'encoding':   detect_text_encoding(header),
        'structure':  detect_structure(header),
    }
```

## Magic Bytes — Known File Signatures

The first few bytes of a file uniquely identify most formats:

```python
MAGIC_SIGNATURES = {
    # Archives / compression
    b'\x1f\x8b':                     'gzip',
    b'BZh':                          'bzip2',
    b'\xfd7zXZ\x00':                 'xz',
    b'PK\x03\x04':                   'zip',
    b'Rar!\x1a\x07':                 'rar',
    b'\x28\xb5\x2f\xfd':             'zstd',
    b'\x04\x22\x4d\x18':             'lz4',
    # Documents / data formats
    b'PAR1':                         'parquet',
    b'ORC':                          'orc',
    b'\x89HDF':                      'hdf5',
    b'SIMPLE  =':                    'fits',           # astronomy
    b'CDF\x01' or b'\xcd\xf0\x01':  'netcdf3',
    # Structured text
    b'\xef\xbb\xbf':                 'utf-8-bom',
    b'\xff\xfe':                     'utf-16-le-bom',
    b'\xfe\xff':                     'utf-16-be-bom',
    # Images
    b'\x89PNG\r\n\x1a\n':            'png',
    b'\xff\xd8\xff':                 'jpeg',
    b'GIF87a' or b'GIF89a':         'gif',
    b'RIFF':                         'wav/avi',
    b'II*\x00' or b'MM\x00*':       'tiff',
    # Binary data
    b'MATLAB 5.0':                   'matlab-mat',
    b'\x93NUMPY':                    'numpy-npy',
    b'PK':                           'npz (zip)',      # .npz is a zip file
    b'\x80\x02':                     'python-pickle2',
    b'\x80\x03':                     'python-pickle3',
    b'\x80\x04':                     'python-pickle4',
    b'\x80\x05':                     'python-pickle5',
    # Database
    b'SQLite format 3':              'sqlite3',
}

def detect_magic(header: bytes) -> str:
    for magic, fmt in MAGIC_SIGNATURES.items():
        if header.startswith(magic):
            return fmt
    # Check longer patterns
    if header[0:4] == b'\x00\x00\x00\x0c' and header[4:8] in (b'ftyp', b'mdat'):
        return 'mp4/mov'
    return 'unknown'
```

## python-magic Library (libmagic bindings)

The most complete magic-byte database:

```bash
pip install python-magic
# Windows: pip install python-magic-bin
```

```python
import magic

# MIME type
mime = magic.from_file('unknown_file', mime=True)
# e.g. 'application/gzip', 'text/csv', 'application/x-hdf'

# Human-readable description
desc = magic.from_file('unknown_file')
# e.g. 'gzip compressed data, last modified: ...'

# From bytes (no file needed)
mime = magic.from_buffer(raw_bytes[:1024], mime=True)
desc = magic.from_buffer(raw_bytes[:1024])
```

## filetype Library (no libmagic dependency)

```bash
pip install filetype
```

```python
import filetype

kind = filetype.guess('unknown_file')
if kind:
    print(kind.mime)       # 'image/png'
    print(kind.extension)  # 'png'

# From bytes
kind = filetype.guess(raw_bytes[:261])   # needs at most 261 bytes

# Type checks
filetype.is_image('file.xyz')
filetype.is_archive('file.xyz')
filetype.is_video('file.xyz')
```

## Compression Detection and Decompression

```python
import gzip, bz2, lzma, zipfile, io
from pathlib import Path

def decompress(data: bytes) -> bytes:
    """Try common compression formats and return decompressed bytes."""
    # gzip
    if data[:2] == b'\x1f\x8b':
        return gzip.decompress(data)
    # bzip2
    if data[:3] == b'BZh':
        return bz2.decompress(data)
    # xz / lzma
    if data[:6] == b'\xfd7zXZ\x00':
        return lzma.decompress(data)
    # zlib (no header — try and see)
    try:
        import zlib
        return zlib.decompress(data)
    except Exception:
        pass
    # zstd
    try:
        import zstandard
        return zstandard.ZstdDecompressor().decompress(data)
    except Exception:
        pass
    return data   # not compressed

def open_any(path: str) -> io.IOBase:
    """Open a file transparently, handling common compressions."""
    p = Path(path)
    if p.suffix == '.gz':
        return gzip.open(path, 'rb')
    if p.suffix == '.bz2':
        return bz2.open(path, 'rb')
    if p.suffix in ('.xz', '.lzma'):
        return lzma.open(path, 'rb')
    if p.suffix == '.zip':
        zf = zipfile.ZipFile(path)
        return zf.open(zf.namelist()[0])
    return open(path, 'rb')
```

## Text Encoding Detection

```python
# chardet: most popular
# pip install chardet
import chardet

with open('unknown.txt', 'rb') as f:
    raw = f.read(10_000)   # read a sample

result = chardet.detect(raw)
# {'encoding': 'UTF-8', 'confidence': 0.99, 'language': ''}

encoding   = result['encoding']    # 'UTF-8', 'ISO-8859-1', 'windows-1252', etc.
confidence = result['confidence']  # 0.0 – 1.0

# charset-normalizer: more accurate alternative
# pip install charset-normalizer
from charset_normalizer import from_bytes, from_path

results = from_bytes(raw)
best = results.best()
print(best.encoding)    # detected encoding
print(str(best))        # decoded string

# Open with detected encoding
with open('unknown.txt', 'rb') as f:
    raw = f.read()
enc = chardet.detect(raw)['encoding'] or 'utf-8'
text = raw.decode(enc, errors='replace')
```

## Structured Format Sniffing

```python
import csv, json, io

def sniff_text_format(text: str) -> str:
    """Try to identify the structure of a text file."""
    stripped = text.strip()

    # JSON
    if stripped.startswith(('{', '[')):
        try:
            json.loads(stripped)
            return 'json'
        except json.JSONDecodeError:
            pass

    # NDJSON
    lines = stripped.splitlines()
    if lines:
        try:
            json.loads(lines[0])
            return 'ndjson'
        except json.JSONDecodeError:
            pass

    # XML / HTML
    if stripped.startswith('<'):
        if '<!DOCTYPE html' in stripped[:200].lower() or '<html' in stripped[:200].lower():
            return 'html'
        return 'xml'

    # CSV / TSV — use csv.Sniffer
    try:
        dialect = csv.Sniffer().sniff(stripped[:2048])
        has_header = csv.Sniffer().has_header(stripped[:2048])
        return f'csv (delimiter={repr(dialect.delimiter)}, header={has_header})'
    except csv.Error:
        pass

    return 'plain text'


def sniff_binary_format(data: bytes) -> str:
    """Try to identify binary format."""
    h = data[:16]

    if h[:4] == b'PAR1':               return 'parquet'
    if h[:3] == b'ORC':                return 'orc'
    if h[:8] == b'\x89HDF\r\n\x1a\n': return 'hdf5'
    if h[:2] == b'\x1f\x8b':          return 'gzip'
    if h[:3] == b'BZh':               return 'bzip2'
    if h[:4] == b'PK\x03\x04':        return 'zip'
    if h[:8] == b'\x93NUMPY':         return 'numpy-npy'
    if h[:1] in (b'\x80',) and h[1:2] in (b'\x02',b'\x03',b'\x04',b'\x05'):
        return f'python-pickle-v{data[1]}'
    if b'MATLAB 5.0' in data[:128]:   return 'matlab-mat'
    if h[:16] == b'SQLite format 3\x00': return 'sqlite3'

    # Try to detect if it's text with non-UTF8 encoding
    try:
        data[:512].decode('utf-8')
        return sniff_text_format(data[:4096].decode('utf-8', errors='replace'))
    except UnicodeDecodeError:
        pass

    return 'unknown binary'
```

## Hexdump and Manual Inspection

```python
def hexdump(data: bytes, width: int = 16, max_rows: int = 32) -> None:
    """Print a hex+ASCII dump for manual inspection."""
    for i in range(0, min(len(data), width * max_rows), width):
        chunk = data[i:i + width]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        asc_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f'{i:08x}  {hex_part:<{width * 3}}  |{asc_part}|')

def byte_frequency(data: bytes) -> dict:
    """Show byte value distribution — helps distinguish text from binary."""
    from collections import Counter
    freq = Counter(data)
    printable = sum(freq[b] for b in range(32, 127))
    null_bytes = freq[0]
    high_bytes = sum(freq[b] for b in range(128, 256))
    return {
        'total':     len(data),
        'printable': printable,
        'printable_pct': printable / len(data),
        'null_bytes': null_bytes,
        'high_bytes': high_bytes,
        'unique_values': len(freq),
        'likely_text': printable / len(data) > 0.9 and null_bytes < len(data) * 0.01,
    }

# Usage
with open('unknown_file', 'rb') as f:
    raw = f.read(1024)

hexdump(raw)
print(byte_frequency(raw))
print(sniff_binary_format(raw))
```

## All-in-One Detector

```python
def detect_format(path_or_bytes) -> dict:
    """Comprehensive format detection."""
    if isinstance(path_or_bytes, (str, Path)):
        with open(path_or_bytes, 'rb') as f:
            data = f.read(4096)
        path = str(path_or_bytes)
    else:
        data = path_or_bytes[:4096]
        path = None

    result = {}

    # 1. python-magic (best if available)
    try:
        import magic
        result['magic_mime'] = magic.from_buffer(data, mime=True)
        result['magic_desc'] = magic.from_buffer(data)
    except ImportError:
        pass

    # 2. filetype
    try:
        import filetype
        kind = filetype.guess(data)
        result['filetype'] = kind.mime if kind else None
    except ImportError:
        pass

    # 3. Manual magic bytes
    result['detected'] = sniff_binary_format(data)

    # 4. Encoding (if text-like)
    freq = byte_frequency(data)
    result['byte_stats'] = freq
    if freq['likely_text']:
        try:
            import chardet
            enc = chardet.detect(data)
            result['encoding'] = enc
        except ImportError:
            pass

    return result
```
