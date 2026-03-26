---
name: python-stdlib-pro
description: Advanced usage of Python's standard library (Pathlib, Regex, JSON). Use for forensic-grade text parsing, atomic file operations, and high-performance data serialization.
---
# Python Standard Library Pro

This skill covers professional-grade patterns for foundational Python modules.

## 1. Pathlib (Object-Oriented FS)

### Atomic Writes
Prevents data corruption by writing to a temp file then renaming.
```python
from pathlib import Path

def atomic_write(path: Path, content: str):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(content, encoding='utf-8')
    tmp.replace(path) # Atomic on same filesystem
```

### Tree Traversal
```python
# Recursive glob for specific extensions
files = list(Path('data/').rglob('*.csv.gz'))

# Building mirrored structures
new_path = output_root / input_file.relative_to(input_root)
new_path.parent.mkdir(parents=True, exist_ok=True)
```

## 2. Regular Expressions (Forensics & Extraction)

### Compiled Patterns (Performance)
Always compile regexes used in loops.
```python
import re
LOG_PATTERN = re.compile(r'(?P<ts>\d{4}-\d{2}-\d{2}) \[(?P<lvl>\w+)\] (?P<msg>.*)')

for line in lines:
    if m := LOG_PATTERN.match(line):
        data = m.groupdict()
```

### Advanced Patterns
- **Named Groups**: `(?P<name>...)`
- **Lookahead**: `(?=...)` (Positive), `(?!...)` (Negative)
- **Verbose**: `re.compile(r"...", re.VERBOSE)` for readable multi-line regex.

## 3. High-Performance JSON

### orjson (The Gold Standard)
3-10x faster than the standard `json` library. Handles NumPy/UUID natively.
```python
import orjson
# Fast serialization
bytes_data = orjson.dumps(my_dict, option=orjson.OPT_SERIALIZE_NUMPY)
# Fast parsing
obj = orjson.loads(bytes_data)
```

### Flattening Nested JSON
```python
import pandas as pd
# Flatten one level of nesting
df = pd.json_normalize(records, record_path=['items'], meta=['id', 'date'])
```

## Common Pitfalls
- **Mutable Defaults**: Never use `def func(a=[])`. Use `None`.
- **Path Slashes**: Never use string concatenation for paths. Use `/`.
- **Regex Backtracking**: Avoid nested quantifiers like `(a+)+` which cause exponential slowdowns.
