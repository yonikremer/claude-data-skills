# struct Module — Complete Reference

## Alignment and Padding

By default, `struct` with a native byte-order prefix (`@` or no prefix) adds padding to match C struct alignment rules.
Use `<`, `>`, or `=` to get packed (no-padding) layout:

```python
import struct

# Native — may add padding between fields
struct.calcsize('@BH')   # likely 4 (pad after B to align H)

# Packed — no padding
struct.calcsize('<BH')   # 3 (1 + 2)
struct.calcsize('>BH')   # 3
```

Use `x` to insert explicit pad bytes when you need to match a format spec that has padding:

```python
fmt = '<B x H'  # byte, 1 pad, uint16 → 4 bytes total
```

## Struct Objects (reuse compiled format)

For tight loops, compile the format once:

```python
record = struct.Struct('<IHH f')  # compile once

with open('data.bin', 'rb') as f:
    size = record.size
    while True:
        raw = f.read(size)
        if len(raw) < size:
            break
        ts, ch, flags, val = record.unpack(raw)
```

## iter_unpack — Stream of records

```python
import struct

fmt = '<IHf'  # 10 bytes per record
with open('data.bin', 'rb') as f:
    data = f.read()

for ts, channel, value in struct.iter_unpack(fmt, data):
    process(ts, channel, value)
```

## pack_into / unpack_from — Work with buffers

```python
import struct, ctypes

# Write into a pre-allocated buffer (zero-copy)
buf = bytearray(1024)
struct.pack_into('<IHf', buf, offset=0, 123456, 7, 3.14)

# Read from a buffer at an offset
ts, ch, val = struct.unpack_from('<IHf', buf, offset=0)
```

## Full Type Code Table

| Code      | Signed | Unsigned | Size   | Notes                                      |
|-----------|--------|----------|--------|--------------------------------------------|
| `b`       | ✓      | —        | 1      |                                            |
| `B`       | —      | ✓        | 1      |                                            |
| `h`       | ✓      | —        | 2      |                                            |
| `H`       | —      | ✓        | 2      |                                            |
| `i`       | ✓      | —        | 4      |                                            |
| `I`       | —      | ✓        | 4      |                                            |
| `l`       | ✓      | —        | 4      | C long (platform-dependent without prefix) |
| `L`       | —      | ✓        | 4      |                                            |
| `q`       | ✓      | —        | 8      |                                            |
| `Q`       | —      | ✓        | 8      |                                            |
| `e`       | —      | —        | 2      | half-precision float (IEEE 754)            |
| `f`       | —      | —        | 4      | single-precision float                     |
| `d`       | —      | —        | 8      | double-precision float                     |
| `?`       | —      | —        | 1      | bool                                       |
| `c`       | —      | —        | 1      | bytes of length 1                          |
| `s`       | —      | —        | n      | `'ns'` → bytes of length n                 |
| `p`       | —      | —        | n      | Pascal string (first byte = length)        |
| `x`       | —      | —        | 1      | pad byte, not returned                     |
| `n` / `N` | ✓/—    | —        | varies | `ssize_t` / `size_t`, native only          |
| `P`       | —      | —        | varies | pointer, native only                       |

## Common Pitfalls

**Strings vs bytes**: `struct` always returns `bytes` for `s` format, not `str`. Decode explicitly:

```python
label_bytes, = struct.unpack('8s', raw)
label = label_bytes.rstrip(b'\x00').decode('ascii')
```

**Single-value unpack**: `unpack` always returns a tuple, even for one value:

```python
(value,) = struct.unpack('<f', raw)   # unpack the tuple
value = struct.unpack('<f', raw)[0]   # or index it
```

**Verify total size before unpacking**:

```python
size = struct.calcsize(fmt)
if len(raw) < size:
    raise ValueError(f"Need {size} bytes, got {len(raw)}")
```

**NaN / Inf in float fields**: Binary floats can hold NaN/Inf — check with `math.isnan()` / `math.isinf()` if the source
may produce them.
