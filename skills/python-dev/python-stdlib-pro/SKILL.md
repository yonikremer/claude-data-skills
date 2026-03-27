---
name: python-stdlib-pro
description: Use when applying advanced patterns from Python's standard library (Pathlib, itertools, collections, contextlib). Ideal for high-performance data manipulation, robust resource management, and complex text parsing.
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

### Advanced Operations
```python
p = Path('data/raw_file.csv.gz')
# Manipulating filename components
new_name = p.with_stem('processed').with_suffix('.json') # data/processed.json

# Glob patterns
all_csvs = list(Path('data/').glob('**/*.csv'))

# File metadata
size = p.stat().st_size
```

## 2. Collections (Specialized Data Types)

### Counter (Frequency Counting)
```python
from collections import Counter
counts = Counter(['a', 'b', 'a', 'c', 'b', 'a'])
print(counts.most_common(2)) # [('a', 3), ('b', 2)]

# Math with counters
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
total = c1 + c2 # Counter({'a': 4, 'b': 3})
```

### Deque (Memory-Efficient Fixed-Size Buffer)
Ideal for "last N items" logic.
```python
from collections import deque
recent_logs = deque(maxlen=100) # Automatically discards old items
recent_logs.append('new_log_line')
```

## 3. Itertools (Efficient Looping)

### Memory-Efficient Slicing & Chaining
```python
from itertools import islice, chain

# Slicing a large generator without loading to memory
subset = islice(large_generator, 10, 20)

# Flattening multiple lists
combined = chain([1, 2], [3, 4], [5]) # [1, 2, 3, 4, 5]
```

### Grouping Data
Requires sorted input.
```python
from itertools import groupby
data = sorted(records, key=lambda x: x['date'])
for date, items in groupby(data, key=lambda x: x['date']):
    print(f"{date}: {len(list(items))} records")
```

## 4. Contextlib (Resource Management)

### Dynamic Context Managers
Use `ExitStack` to manage an unknown number of open resources.
```python
from contextlib import ExitStack

def process_files(file_paths):
    with ExitStack() as stack:
        files = [stack.enter_context(open(p)) for p in file_paths]
        # All files are automatically closed when exiting the stack
```

### Suppressing Specific Errors
```python
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove('non_existent_file.txt') # No exception raised
```

## 5. Functools (Higher-Order Functions)

### Effortless Memoization
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(x, y):
    return x ** y # Result cached for future calls
```

### Function Factories
```python
from functools import partial
def power(base, exp): return base ** exp
square = partial(power, exp=2)
print(square(10)) # 100
```

## 6. Dataclasses (Clean Data Structures)

```python
from dataclasses import dataclass, field, asdict

@dataclass
class User:
    id: int
    name: str
    tags: list = field(default_factory=list) # Safe mutable default

user = User(1, 'Alice')
data = asdict(user) # {'id': 1, 'name': 'Alice', 'tags': []}
```

## 7. Performance (Bisect & Heapq)

### Sorted Insertion (Binary Search)
```python
import bisect
scores = [10, 20, 30]
bisect.insort(scores, 25) # scores is now [10, 20, 25, 30]
```

### Finding N-Extreme Elements
```python
import heapq
data = [10, 2, 33, 1, 44, 22]
top_3 = heapq.nlargest(3, data) # [44, 33, 22]
```

## 8. Robust File Operations (Shutil & Tempfile)

```python
import shutil
import tempfile

# Robust copying (preserves metadata)
shutil.copy2('src.txt', 'dst.txt')

# Safe temporary directory
with tempfile.TemporaryDirectory() as tmp_dir:
    # Do work in tmp_dir
    pass # Automatically deleted on exit
```

## 9. High Performance JSON (Beyond Stdlib)

### orjson (The Gold Standard)
3-10x faster than the standard `json` library.
```python
import orjson
# Fast serialization
bytes_data = orjson.dumps(my_dict, option=orjson.OPT_SERIALIZE_NUMPY)
# Fast parsing
obj = orjson.loads(bytes_data)
```

## Common Pitfalls
- **Mutable Defaults**: Never use `def func(a=[])`. Use `dataclass` or `a=None`.
- **Path Slashes**: Never use string concatenation for paths. Use `pathlib.Path / "file"`.
- **Regex Backtracking**: Avoid nested quantifiers like `(a+)+` which cause exponential slowdowns.
