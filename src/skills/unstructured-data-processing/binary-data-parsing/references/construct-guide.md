# construct Library — Complete Reference

Install: `pip install construct`

## Core Building Blocks

### Primitive Types

```python
from construct import (
    # Integers — naming: Int<bits><u/s><l/b> (l=little, b=big)
    Int8ub, Int8sb,
    Int16ub, Int16ul, Int16sb, Int16sl,
    Int32ub, Int32ul, Int32sb, Int32sl,
    Int64ub, Int64ul, Int64sb, Int64sl,
    # Floats
    Float32b, Float32l, Float64b, Float64l,
    # Bytes
    Bytes, GreedyBytes,
    # Strings
    PaddedString, GreedyString,
    # Boolean
    Flag,
)
```

### Struct

```python
from construct import Struct, Int32ul, Float32l, Bytes

Point = Struct(
    "x" / Float32l,
    "y" / Float32l,
)

Header = Struct(
    "magic"   / Bytes(4),
    "version" / Int32ul,
    "count"   / Int32ul,
)

result = Header.parse(b'MYFT\x01\x00\x00\x00\x0a\x00\x00\x00')
result.magic    # b'MYFT'
result.version  # 1
result.count    # 10
```

### Array — fixed count

```python
from construct import Array, Int16ul

# Fixed count
ThreePoints = Array(3, Point)

# Count from context (earlier field)
Records = Struct(
    "count"   / Int32ul,
    "records" / Array(lambda ctx: ctx.count, Point),
)
```

### RepeatUntil / GreedyRange — variable count

```python
from construct import RepeatUntil, GreedyRange

# Repeat until a sentinel value
NullTerminated = RepeatUntil(lambda obj, lst, ctx: obj == 0, Int8ub)

# Repeat until end of stream
AllRecords = GreedyRange(Point)
```

### Switch — conditional types

```python
from construct import Switch, Enum, Int8ub

TypeId = Enum(Int8ub, INTEGER=1, FLOAT=2, STRING=3)

Payload = Switch(
    lambda ctx: ctx.type_id,
    {
        "INTEGER": Int32sl,
        "FLOAT":   Float32l,
        "STRING":  PaddedString(16, 'utf8'),
    }
)

Packet = Struct(
    "type_id" / TypeId,
    "payload" / Payload,
)
```

### If / IfThenElse — optional fields

```python
from construct import If, IfThenElse, Int32ul

Record = Struct(
    "flags"     / Int8ub,
    "timestamp" / Int32ul,
    "extra"     / If(lambda ctx: ctx.flags & 0x01, Float32l),
)
```

### Enum

```python
from construct import Enum, Int8ub

Status = Enum(Int8ub,
    OK      = 0,
    WARNING = 1,
    ERROR   = 2,
)

result = Status.parse(b'\x01')
result  # 'WARNING'
```

### BitStruct — bit-level fields

```python
from construct import BitStruct, BitsInteger, Flag, Nibble, Padding

# Total must be a multiple of 8 bits
StatusByte = BitStruct(
    "error"    / Flag,          # 1 bit
    "overflow" / Flag,          # 1 bit
    "ready"    / Flag,          # 1 bit
    "channel"  / BitsInteger(2), # 2 bits
    "mode"     / BitsInteger(3), # 3 bits
)                               # = 8 bits total

result = StatusByte.parse(b'\xA3')
result.error    # True/False
result.channel  # 0-3
result.mode     # 0-7
```

### Prefixed — length-prefixed blobs

```python
from construct import Prefixed, Int16ul, GreedyBytes

# 2-byte length prefix followed by that many bytes
LengthPrefixedBlob = Prefixed(Int16ul, GreedyBytes)

Packet = Struct(
    "header"  / Int32ul,
    "payload" / Prefixed(Int16ul, GreedyBytes),
)
```

## Adapters and Transforms

### ExprAdapter — inline transformation

```python
from construct import ExprAdapter, Int32ul

# Scale raw integer by factor
TemperatureC = ExprAdapter(Int16sl,
    decoder=lambda obj, ctx: obj / 100.0,
    encoder=lambda obj, ctx: int(obj * 100),
)
```

### Tunnel — parse payload as another format

```python
from construct import Tunnel, Compressed, GreedyBytes
import zlib

ZlibPayload = Tunnel(GreedyBytes,
    decoder=zlib.decompress,
    encoder=zlib.compress,
)
```

## Parsing and Building

```python
# Parse from bytes
result = MyFormat.parse(raw_bytes)

# Parse from file
with open('data.bin', 'rb') as f:
    result = MyFormat.parse_stream(f)

# Build bytes from dict/Container
raw = MyFormat.build({"magic": b'MYFT', "version": 1, "count": 5})

# Get size (for fixed-size formats)
size = MyFormat.sizeof()  # raises if variable-size
```

## Debugging

```python
from construct import Debugger

# Wraps any construct to print debug info on parse
DebugHeader = Debugger(Header)

# Or use Probe to inspect context mid-parse
from construct import Probe

Record = Struct(
    "type_id" / Int8ub,
    Probe(),       # prints context here
    "value"  / Int32ul,
)
```
