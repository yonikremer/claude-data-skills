# bytes, bytearray, memoryview, and bitarray — Complete Reference

## bytes and bytearray

`bytes` is immutable; `bytearray` is mutable. Both support the same read operations.

### Creation

```python
# Literals
b'\x00\xFF\xde\xad'
b'ASCII text'

# From integer (zero-filled)
bytes(8)              # b'\x00\x00\x00\x00\x00\x00\x00\x00'
bytearray(8)

# From iterable of ints (0–255)
bytes([0, 1, 254, 255])

# From hex string
bytes.fromhex('deadbeef')         # b'\xde\xad\xbe\xef'
bytes.fromhex('de ad be ef')      # spaces are allowed

# From file
with open('data.bin', 'rb') as f:
    data = f.read()
```

### Indexing and Slicing

```python
data = b'\x00\x01\x02\x03\x04\x05'

data[0]          # 0    — single index returns int, not bytes
data[-1]         # 5
data[2:5]        # b'\x02\x03\x04'  — slice returns bytes/bytearray
data[::2]        # b'\x00\x02\x04'  — every other byte
```

### Conversion

```python
# To/from hex
data.hex()               # 'deadbeef...'
data.hex(':')            # 'de:ad:be:ef'   (separator, Python 3.8+)
data.hex(':', 2)         # 'dead:beef'     (bytes_per_sep, Python 3.8+)

# To list of ints
list(data)               # [0, 1, 2, 3, 4, 5]

# To int — replaces struct for simple single-value cases
int.from_bytes(b'\x00\x01', byteorder='big')       # 1
int.from_bytes(b'\x01\x00', byteorder='little')    # 1
int.from_bytes(b'\xff\xff', byteorder='big', signed=True)   # -1

# From int
(1024).to_bytes(2, byteorder='big')          # b'\x04\x00'
(1024).to_bytes(2, byteorder='little')       # b'\x00\x04'
(-1).to_bytes(2, byteorder='big', signed=True)  # b'\xff\xff'

# Auto-size (Python 3.11+)
n = 0xDEADBEEF
n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
```

### Searching

```python
data = b'\x00\xAA\xBB\xAA\xBB\xFF'

data.find(b'\xAA\xBB')       # 1   (-1 if not found)
data.index(b'\xAA\xBB')      # 1   (raises ValueError if not found)
data.rfind(b'\xAA\xBB')      # 3   (search from right)
data.count(b'\xAA')          # 2

# Find all occurrences
def find_all(data: bytes, pattern: bytes):
    pos, positions = 0, []
    while True:
        pos = data.find(pattern, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += len(pattern)
    return positions
```

### bytearray — Mutable Operations

```python
buf = bytearray(b'\x00' * 8)

# In-place modification
buf[0] = 0xFF
buf[2:4] = b'\xDE\xAD'

# Append / extend
buf.append(0x01)
buf.extend(b'\x02\x03')

# Replace a slice
buf[0:4] = b'\xCA\xFE\xBA\xBE'

# Insert a byte
buf.insert(2, 0x99)

# Delete bytes
del buf[2:4]

# Efficient pre-allocated buffer for building output
out = bytearray()
for record in records:
    out += struct.pack('<If', record.ts, record.val)
with open('out.bin', 'wb') as f:
    f.write(out)
```

## memoryview — Zero-Copy Slicing

`memoryview` exposes a buffer without copying. Essential when working with large mmap regions, socket data, or when passing sub-slices to struct.

```python
import struct

data = bytearray(b'\x00\x01\x02\x03\x04\x05\x06\x07')
mv = memoryview(data)

# Slice without copy
chunk = mv[2:6]           # memoryview, not bytes — no allocation
bytes(chunk)              # b'\x02\x03\x04\x05' — copy only when needed

# Use directly with struct (avoids copy)
ts, val = struct.unpack_from('<HH', mv, offset=2)

# Cast to a different item type
mv_int16 = mv.cast('H')   # view same bytes as uint16 array
mv_int16[0]               # first uint16

# Write through memoryview (if source is bytearray)
mv[0:2] = b'\xFF\xFE'
```

## io.BytesIO — In-Memory Binary Stream

Treat a `bytes` object as a seekable file. Useful for parsing with stream-oriented code or constructing binary output in memory.

```python
import io, struct

# Read from in-memory bytes
data = b'\x01\x00\x00\x00\x02\x00\x00\x00'
stream = io.BytesIO(data)

a = struct.unpack('<I', stream.read(4))[0]   # 1
b = struct.unpack('<I', stream.read(4))[0]   # 2
stream.seek(0)                               # rewind
stream.tell()                                # current position

# Build binary output in memory
out = io.BytesIO()
out.write(struct.pack('>4sI', b'MYFT', 42))
out.write(b'\x00' * 16)
result: bytes = out.getvalue()
```

---

## bitarray

Install: `pip install bitarray`

Stores bits packed into machine words — 8× more memory-efficient than a Python `list` of bools, and operations are vectorized in C.

### Creation

```python
from bitarray import bitarray
from bitarray.util import int2ba, ba2int, zeros, ones, ba2hex, hex2ba

# From binary string
a = bitarray('10110100')

# Uninitialized, then fill
a = bitarray(8)
a.setall(0)             # all zeros
a = zeros(8)            # same, but initialized
a = ones(8)             # all ones

# From bytes (bit order: MSB first by default)
a = bitarray()
a.frombytes(b'\xB4')    # 10110100

# From integer
a = int2ba(180, length=8)         # bitarray('10110100')
a = int2ba(180, length=8, endian='little')  # LSB first

# From hex
a = hex2ba('b4ff')                # 16 bits
```

### Indexing, Slicing, Iteration

```python
a = bitarray('10110100')

a[0]           # True  (MSB)
a[-1]          # False
a[2:5]         # bitarray('110')
a[::2]         # every other bit

# Iterate
for bit in a:
    print(int(bit))

# Convert to list of bools
list(a)        # [True, False, True, True, False, True, False, False]
```

### Bitwise Operations

```python
a = bitarray('10110100')
b = bitarray('11001010')

a & b          # AND  → bitarray('10000000')
a | b          # OR   → bitarray('11111110')
a ^ b          # XOR  → bitarray('01111110')
~a             # NOT  → bitarray('01001011')

# In-place
a &= b
a |= b
a ^= b

# Shift (no built-in — use slicing)
a << 2         # not supported; do: bitarray('00') + a[:-2]
```

### Searching

```python
a = bitarray('1010110101')

# Find all positions of a pattern
a.search(bitarray('101'))     # [0, 2, 7] — list of start indices

# Count set/unset bits
a.count(1)    # number of 1s
a.count(0)    # number of 0s
a.any()       # True if any bit is 1
a.all()       # True if all bits are 1
```

### Conversion

```python
# To/from bytes
raw = a.tobytes()       # pads to byte boundary on the right
a2 = bitarray()
a2.frombytes(raw)

# To/from int
ba2int(a)               # unsigned integer, MSB first
int2ba(42, length=8)

# To/from hex
ba2hex(a)               # hex string (must be multiple of 4 bits)
hex2ba('deadbeef')

# To numpy bool array
import numpy as np
arr = np.frombuffer(a.tobytes(), dtype=np.uint8)
# or use bitarray.util.ba2np (if available) or unpack manually
```

### Working with Large Bit Arrays

```python
from bitarray import bitarray

# Read a binary file as bits
bits = bitarray()
with open('data.bin', 'rb') as f:
    bits.fromfile(f)               # reads entire file

# Write bits to file (pads to byte boundary)
with open('output.bin', 'wb') as f:
    bits.tofile(f)

# Memory-efficient: 1M bits = 125 KB
big = zeros(1_000_000)

# Bulk set via slice assignment
big[100:200] = ones(100)
big[100:200] = zeros(100)
big[100:200] = bitarray('1' * 100)
```

### Huffman Coding

```python
from bitarray.util import huffman_code, encode, decode

# Build code from symbol frequencies
freq = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
code = huffman_code(freq)
# code = {'a': bitarray('0'), 'b': bitarray('101'), ...}

# Encode a sequence
text = 'abcde'
encoded = encode(code, text)      # bitarray

# Decode
decoded = decode(code, encoded)   # ['a', 'b', 'c', 'd', 'e']
```

### endian parameter

By default, `bitarray` stores bits in MSB-first order within each byte (same as network byte order). For LSB-first (common in some hardware/RF protocols):

```python
a = bitarray('10110100', endian='little')  # LSB of byte is bit[0]
a.frombytes(b'\xB4')                       # bit layout differs
```

Always be explicit about endianness when interoperating with hardware data.
