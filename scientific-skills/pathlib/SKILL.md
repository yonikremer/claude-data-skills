---
name: pathlib
description: File system operations in Python using pathlib.Path, shutil, and os. Use for building paths, reading/writing files, listing directories, globbing, moving/copying/deleting files, and working with file metadata. Pathlib is the modern replacement for os.path string manipulation.
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# pathlib and File System Operations

## Path Basics

```python
from pathlib import Path

# Create paths
p = Path('/data/raw/2024/data.csv')
p = Path('relative/path/file.txt')
p = Path.home()              # user home directory (~)
p = Path.cwd()               # current working directory

# Build paths with / operator
data_dir = Path('/data')
file = data_dir / 'raw' / '2024' / 'data.csv'

# From __file__ (common in scripts to find paths relative to the script)
HERE = Path(__file__).parent
CONFIG = HERE / 'config' / 'settings.env'
DATA   = HERE.parent / 'data'
```

## Path Properties

```python
p = Path('/data/raw/2024/measurements.csv.gz')

p.name          # 'measurements.csv.gz'
p.stem          # 'measurements.csv'    (name without last suffix)
p.suffix        # '.gz'
p.suffixes      # ['.csv', '.gz']
p.parent        # Path('/data/raw/2024')
p.parents[0]    # Path('/data/raw/2024')
p.parents[1]    # Path('/data/raw')
p.parts         # ('/', 'data', 'raw', '2024', 'measurements.csv.gz')
p.root          # '/'
p.anchor        # '/'  (drive + root on Windows: 'C:\\')
str(p)          # '/data/raw/2024/measurements.csv.gz'
p.as_posix()    # always forward slashes (useful on Windows)
```

## Existence and Type Checks

```python
p.exists()          # True if path exists
p.is_file()         # True if regular file
p.is_dir()          # True if directory
p.is_symlink()      # True if symlink
p.is_absolute()     # True if absolute path
p.resolve()         # resolve symlinks + make absolute
```

## Reading and Writing

```python
# Text
text = p.read_text(encoding='utf-8')
p.write_text('hello\n', encoding='utf-8')
p.write_text(content, encoding='utf-8')   # overwrites

# Binary
raw = p.read_bytes()
p.write_bytes(b'\x00\x01\x02')

# Line-by-line (memory efficient)
with p.open(encoding='utf-8') as f:
    for line in f:
        process(line.rstrip())

# Append
with p.open('a', encoding='utf-8') as f:
    f.write('new line\n')
```

## Listing and Globbing

```python
d = Path('/data')

# List immediate children
list(d.iterdir())                      # all entries
[p for p in d.iterdir() if p.is_file()]
[p for p in d.iterdir() if p.is_dir()]

# Glob — non-recursive
list(d.glob('*.csv'))                  # CSV files in d
list(d.glob('2024/*.parquet'))         # parquet in subdirectory

# rglob — recursive (equivalent to **/)
list(d.rglob('*.csv'))                 # all CSV files anywhere under d
list(d.rglob('*.csv.gz'))
list(d.rglob('data_*.parquet'))        # pattern matching

# Sorted by modification time (most recent first)
files = sorted(d.rglob('*.log'), key=lambda p: p.stat().st_mtime, reverse=True)

# Filter by size
large = [p for p in d.rglob('*.csv') if p.stat().st_size > 100_000_000]  # > 100 MB
```

## File Metadata

```python
stat = p.stat()

stat.st_size     # size in bytes
stat.st_mtime    # last modified (Unix timestamp)
stat.st_ctime    # created (Windows) / metadata changed (Unix)
stat.st_atime    # last accessed

# Human-readable
import datetime
modified = datetime.datetime.fromtimestamp(stat.st_mtime)
size_mb  = stat.st_size / 1e6

# Quick size check
p.stat().st_size > 0    # non-empty file
```

## Create, Move, Copy, Delete

```python
from pathlib import Path
import shutil

# Create directories
Path('output/2024/jan').mkdir(parents=True, exist_ok=True)

# Rename / move (within same filesystem — fast)
p.rename(p.parent / 'new_name.csv')       # raises if destination exists
p.replace(p.parent / 'new_name.csv')      # overwrites destination

# Copy (use shutil for cross-filesystem or directory copies)
shutil.copy(src, dst)         # copy file, preserve permissions
shutil.copy2(src, dst)        # copy file, preserve all metadata
shutil.copytree(src_dir, dst_dir)                         # copy entire directory
shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)     # merge into existing dir

# Move (works across filesystems)
shutil.move(src, dst)

# Delete
p.unlink()                    # delete file (raises if missing)
p.unlink(missing_ok=True)     # delete file (silent if missing)
p.rmdir()                     # delete empty directory
shutil.rmtree(dir_path)       # delete directory and all contents (careful!)

# Safe delete pattern
if p.exists():
    p.unlink()
```

## Common Patterns

### Process all files in a directory tree

```python
from pathlib import Path
import pandas as pd

data_dir = Path('data/raw')
results = []

for csv_file in sorted(data_dir.rglob('*.csv')):
    df = pd.read_csv(csv_file)
    df['source_file'] = csv_file.name
    results.append(df)

combined = pd.concat(results, ignore_index=True)
```

### Build output path mirroring input structure

```python
def mirror_path(src: Path, src_root: Path, dst_root: Path) -> Path:
    """Recreate the directory structure under a new root."""
    relative = src.relative_to(src_root)
    return dst_root / relative

src  = Path('data/raw/2024/jan/file.csv')
dest = mirror_path(src, Path('data/raw'), Path('data/processed'))
# → Path('data/processed/2024/jan/file.csv')
dest.parent.mkdir(parents=True, exist_ok=True)
```

### Atomic write (write to temp, then rename)

```python
import tempfile

def atomic_write(path: Path, content: str):
    """Write to a temp file first, then rename — prevents partial writes."""
    tmp = path.with_suffix('.tmp')
    tmp.write_text(content, encoding='utf-8')
    tmp.replace(path)   # atomic on same filesystem
```

### Find most recent file matching a pattern

```python
def latest_file(directory: Path, pattern: str) -> Path:
    files = list(directory.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matching {pattern} in {directory}")
    return max(files, key=lambda p: p.stat().st_mtime)

latest_log = latest_file(Path('logs'), '*.log')
```

### Disk usage

```python
import shutil

total, used, free = shutil.disk_usage('/')
print(f"Free: {free / 1e9:.1f} GB")

# Size of a directory tree
def dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())

print(f"data/ is {dir_size(Path('data')) / 1e6:.1f} MB")
```

### Temporary files and directories

```python
import tempfile
from pathlib import Path

# Temp file (auto-deleted on close)
with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
    tmp_path = Path(f.name)
    f.write(b'id,val\n1,3.14\n')
# file persists until you delete it
tmp_path.unlink()

# Temp directory (auto-deleted on context exit)
with tempfile.TemporaryDirectory() as tmp_dir:
    work_dir = Path(tmp_dir)
    (work_dir / 'output.csv').write_text('result')
    process(work_dir)
# tmp_dir deleted here
```
