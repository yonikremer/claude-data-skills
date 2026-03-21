---
name: binary-data-parsing
description: Parse and manipulate raw binary data, byte streams, and custom binary file formats. Use when working with binary protocols, sensor/instrument output, legacy file formats, network packets, or any data that requires bit/byte-level access. Covers Python bytes/bytearray/memoryview (stdlib), struct (stdlib), bitarray (efficient bit arrays), construct (declarative parsing), bitstring (bit streams), and mmap (large files). Not for standard formats like Parquet/HDF5 — use polars or zarr for those.
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# Binary Data Parsing

## Overview

Tools for reading, parsing, and writing raw binary data in Python. Pick the right tool for the job:

| Approach | Best For | Library |
|----------|----------|---------|
| `bytes` / `bytearray` / `memoryview` | Slicing, searching, hex conversion, in-place mutation | stdlib |
| `int.from_bytes` / `int.to_bytes` | Converting raw bytes ↔ integers without struct | stdlib |
| `struct` | Fixed-width records, known format specs | stdlib |
| `bitarray` | Large dense bit arrays, set operations, Huffman coding | `pip install bitarray` |
| `construct` | Complex/nested formats, variable-length fields, declarative specs | `pip install construct` |
| `bitstring` | Bit-stream reading with mixed-width fields, network protocols | `pip install bitstring` |
| `mmap` | Large binary files, random access without loading to RAM | stdlib |

## Quick Start

### bytes / bytearray — slicing, searching, converting

```python
# bytes is immutable; bytearray is mutable
data = b'\x00\x01\xde\xad\xbe\xef'

# Indexing returns an int
data[0]          # 0
data[2]          # 222 (0xde)

# Slicing returns bytes
data[2:6]        # b'\xde\xad\xbe\xef'

# Hex conversion
data.hex()                   # '0001deadbeef'
data.hex(':')                # '00:01:de:ad:be:ef'
bytes.fromhex('deadbeef')    # b'\xde\xad\xbe\xef'

# Search
data.find(b'\xde\xad')       # 2  (-1 if not found)

# Convert bytes ↔ int (no struct needed for simple cases)
int.from_bytes(b'\x00\x01',  byteorder='big')     # 1
int.from_bytes(b'\x01\x00',  byteorder='little')  # 1
(258).to_bytes(2, byteorder='big')                # b'\x01\x02'

# bytearray for in-place mutation
buf = bytearray(b'\x00' * 8)
buf[0:4] = b'\xde\xad\xbe\xef'

# memoryview — zero-copy slice into a buffer (useful with mmap / socket data)
mv = memoryview(buf)
chunk = mv[2:6]              # no copy made
bytes(chunk)                 # b'\xbe\xef\x00\x00'
```

### bitarray — dense bit arrays and set operations

```python
from bitarray import bitarray
from bitarray.util import int2ba, ba2int, zeros, ba2hex, hex2ba

# Create
a = bitarray('10110100')       # from binary string
b = bitarray(8)                # uninitialized, 8 bits
b.setall(0)

# From bytes / integers
a = bitarray()
a.frombytes(b'\xB4')           # 10110100
ba2int(a)                      # 180
int2ba(180, length=8)          # bitarray('10110100')

# Hex
ba2hex(a)                      # 'b4'
hex2ba('b4')                   # bitarray('10110100')

# Bitwise operations
c = a & b
c = a | b
c = a ^ b
c = ~a

# Indexing and slicing
a[0]           # True (MSB)
a[2:5]         # bitarray('110')

# Search for a pattern
a.search(bitarray('101'))      # [0, ...]  list of start positions

# Count
a.count(1)     # number of set bits (popcount)
a.count(0)     # number of zero bits

# Pack/unpack from bytes (efficient bulk I/O)
raw = b'\xB4\xFF'
bits = bitarray()
bits.frombytes(raw)            # 16 bits
bits.tobytes()                 # b'\xb4\xff'

# Huffman encoding (built-in)
from bitarray.util import huffman_code
freq = {'a': 10, 'b': 5, 'c': 3}
code = huffman_code(freq)      # {'a': bitarray('0'), 'b': bitarray('10'), ...}
```

### struct — Fixed-width records

```python
import struct

# Format string: '<' = little-endian, 'I' = uint32, 'f' = float32, '4s' = 4-byte string
fmt = '<I f 4s'
size = struct.calcsize(fmt)  # bytes per record

with open('data.bin', 'rb') as f:
    raw = f.read(size)
    timestamp, value, label = struct.unpack(fmt, raw)

# Read many records at once
import numpy as np
data = np.frombuffer(raw_bytes, dtype=np.dtype([
    ('timestamp', '<u4'),
    ('value', '<f4'),
    ('label', 'S4'),
]))
```

### construct — Declarative parsing

```python
from construct import Struct, Int32ul, Float32l, Bytes, Array, Prefixed, GreedyBytes

# Define format declaratively
Header = Struct(
    "magic" / Bytes(4),
    "version" / Int32ul,
    "record_count" / Int32ul,
)

Record = Struct(
    "timestamp" / Int32ul,
    "value" / Float32l,
)

FileFormat = Struct(
    "header" / Header,
    "records" / Array(lambda ctx: ctx.header.record_count, Record),
)

with open('data.bin', 'rb') as f:
    result = FileFormat.parse_stream(f)

print(result.header.version)
print(result.records[0].value)
```

### bitstring — Bit-level access

```python
from bitstring import BitStream, ConstBitStream

bs = ConstBitStream(filename='data.bin')

# Read specific bit widths
sync_word = bs.read('uint:16')
flags     = bs.read('bin:8')       # as binary string e.g. '10110010'
value     = bs.read('floatbe:32')  # big-endian float

# Check individual flags
bs.pos = 0
header_byte = bs.read('uint:8')
flag_a = bool(header_byte & 0b10000000)
flag_b = bool(header_byte & 0b01000000)
```

### mmap — Large file random access

```python
import mmap, struct

RECORD_SIZE = 12  # bytes per record

with open('large.bin', 'rb') as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        n_records = len(mm) // RECORD_SIZE

        # Jump directly to record 100000 without reading everything
        offset = 100000 * RECORD_SIZE
        raw = mm[offset:offset + RECORD_SIZE]
        ts, val, flags = struct.unpack('<IIf', raw)  # wait, adjust to your fmt
```

## Format String Reference (struct)

### Byte Order Prefixes

| Prefix | Meaning |
|--------|---------|
| `<` | little-endian (x86, most modern hardware) |
| `>` | big-endian (network order, some instruments) |
| `=` | native byte order |
| `!` | network (big-endian) |

### Type Codes

| Code | C Type | Python | Size |
|------|--------|--------|------|
| `b` / `B` | signed/unsigned char | int | 1 |
| `h` / `H` | signed/unsigned short | int | 2 |
| `i` / `I` | signed/unsigned int | int | 4 |
| `q` / `Q` | signed/unsigned long long | int | 8 |
| `f` | float | float | 4 |
| `d` | double | float | 8 |
| `s` | char[] | bytes | n (use `4s` for 4 bytes) |
| `x` | pad byte | — | 1 |
| `?` | bool | bool | 1 |

Repeat with count prefix: `'10f'` = 10 floats, `'4s'` = 4-byte string.

## Common Patterns

### Read a file header then variable records

```python
import struct

HEADER_FMT = '>4sHHI'   # magic(4), major(2), minor(2), n_records(4)
RECORD_FMT = '>Qd'      # timestamp_us(8), value(8)

with open('data.bin', 'rb') as f:
    hdr_size = struct.calcsize(HEADER_FMT)
    magic, major, minor, n_records = struct.unpack(HEADER_FMT, f.read(hdr_size))

    assert magic == b'MYFT', f"Bad magic: {magic}"

    rec_size = struct.calcsize(RECORD_FMT)
    records = [
        struct.unpack(RECORD_FMT, f.read(rec_size))
        for _ in range(n_records)
    ]
```

### Bulk read into numpy (fastest for uniform records)

```python
import numpy as np

dtype = np.dtype([
    ('timestamp_us', '>u8'),
    ('value',        '>f8'),
    ('status',       '>u2'),
])

with open('data.bin', 'rb') as f:
    f.seek(header_size)
    arr = np.frombuffer(f.read(), dtype=dtype)

# Now use as structured numpy array
print(arr['value'].mean())
import pandas as pd
df = pd.DataFrame(arr)
```

### Handle unknown/variable-length chunks

```python
from construct import Struct, Bytes, Int16ul, Switch, GreedyBytes, Const

Chunk = Struct(
    "type_id" / Int16ul,
    "length"  / Int16ul,
    "payload" / Bytes(lambda ctx: ctx.length),
)

def parse_chunks(data: bytes):
    offset = 0
    chunks = []
    while offset < len(data):
        chunk = Chunk.parse(data[offset:])
        chunks.append(chunk)
        offset += 4 + chunk.length  # header(4) + payload
    return chunks
```

### Bit flags / bitmask extraction

```python
# Without bitstring — standard Python
def decode_status_byte(byte: int) -> dict:
    return {
        'error':    bool(byte & 0x80),
        'overflow': bool(byte & 0x40),
        'ready':    bool(byte & 0x20),
        'channel':  (byte & 0x18) >> 3,   # bits 4-3
        'mode':     byte & 0x07,           # bits 2-0
    }

status = decode_status_byte(raw_bytes[offset])
```

### Write binary data

```python
import struct

records = [(1700000000, 3.14), (1700000001, 2.71)]

with open('output.bin', 'wb') as f:
    # Write header
    f.write(struct.pack('>4sI', b'MYFT', len(records)))
    # Write records
    for ts, val in records:
        f.write(struct.pack('>Qd', ts, val))
```

## Debugging Strategies

```python
# Inspect first N bytes as hex
def hexdump(data: bytes, width: int = 16):
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        asc_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f'{i:08x}  {hex_part:<{width*3}}  {asc_part}')

with open('unknown.bin', 'rb') as f:
    hexdump(f.read(256))

# Try both endiannesses
raw = b'\x01\x00\x00\x00'
print(struct.unpack('<I', raw))  # (1,)   — little-endian
print(struct.unpack('>I', raw))  # (16777216,) — big-endian
```

## References

- `references/bytes-bitarray-guide.md` — bytes/bytearray/memoryview operations, int.from_bytes, io.BytesIO, bitarray advanced usage
- `references/struct-guide.md` — full struct format string reference, alignment, padding, edge cases
- `references/construct-guide.md` — construct library: enums, switches, conditionals, adapters, tunneling
- `references/patterns.md` — domain-specific patterns: sensor data, network protocols, legacy formats, Python 2 pickles
