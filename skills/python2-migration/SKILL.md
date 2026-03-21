---
name: python2-migration
description: Migrates legacy Python 2 code to Python 3. Use when modernizing old scripts or reading Python 2-specific data files. Do NOT use for general refactoring (use refactoring) or for new project development.
---
# Python 2 → Python 3 Migration

## Automated Migration with 2to3

`2to3` is bundled with Python and rewrites most syntax automatically:

```bash
# Preview changes (dry run)
2to3 old_script.py

# Apply changes in-place (-w), keep backup (-n skips backup)
2to3 -w old_script.py

# Apply to entire directory
2to3 -w src/

# Run only specific fixers
2to3 -f print -f unicode -w old_script.py

# List all available fixers
2to3 -l
```

After running `2to3`, the code will be Python 3 only. For files that must run on both versions (rare), use `six` or `future`.

## Most Common Breaking Changes

### print statement → print function

```python
# Python 2
print "hello"
print "a", "b"
print >>sys.stderr, "error"

# Python 3
print("hello")
print("a", "b")
print("error", file=sys.stderr)
```

### Integer division

```python
# Python 2: 3/2 == 1  (integer division)
# Python 3: 3/2 == 1.5

# Fix: use // for explicit integer division
result = a // b       # floor division — works in both
result = a / b        # now always float in Python 3

# If old code expected integer division:
result = int(a / b)   # or a // b
```

### str / unicode / bytes

```python
# Python 2: str = bytes, unicode = text
# Python 3: str = text (unicode), bytes = binary

# Python 2 code pattern:
s = u"hello"         # unicode string
b = "hello"          # bytes (str)

# Python 3: u"..." is valid but redundant — both are str
s = "hello"          # str (unicode)
b = b"hello"         # bytes

# Reading files
# Python 2: open() returns bytes by default
# Python 3: open() returns str (unicode) by default
f = open('file.txt', 'r', encoding='utf-8')   # explicit encoding

# If old code reads binary and calls .decode():
data = f.read()           # str in Python 3 — no .decode() needed
data = f.read().decode()  # WRONG in Python 3 — str has no .decode()

# Binary files still need 'rb'
with open('file.bin', 'rb') as f:
    raw = f.read()   # bytes in both Python 2 and 3
```

### dict methods returning views vs lists

```python
# Python 2: .keys(), .values(), .items() return lists
# Python 3: return view objects

# Old code that relies on list behavior:
keys = d.keys()
keys.sort()         # AttributeError in Python 3 — views have no .sort()

# Fix:
keys = sorted(d.keys())
keys = list(d.keys())     # explicit list if needed

# dict.iteritems(), .itervalues(), .iterkeys() — removed in Python 3
# Python 2:
for k, v in d.iteritems():  ...
# Python 3:
for k, v in d.items():      ...
```

### range / xrange

```python
# Python 2: range() returns list, xrange() returns iterator
# Python 3: range() returns iterator (like xrange), xrange() removed

# Fix: just use range() everywhere
for i in range(1000000):   # memory-efficient in Python 3
    ...

# If old code does list operations on range:
r = range(10)
r[3]        # works in Python 3 (range supports indexing)
list(r)     # explicit list when needed
```

### map / filter / zip — now return iterators

```python
# Python 2: return lists
# Python 3: return iterators

# If old code indexes result:
result = map(str, nums)
result[0]          # TypeError in Python 3

# Fix:
result = list(map(str, nums))
# Or prefer list comprehensions (more Pythonic):
result = [str(n) for n in nums]
```

### Exception syntax

```python
# Python 2 (both forms worked):
except ValueError, e:     # old syntax — SyntaxError in Python 3
except ValueError as e:   # new syntax — works in both 2.6+ and 3

# Raise
raise ValueError, "message"  # Python 2 only
raise ValueError("message")  # works in both
```

### urllib / urllib2 split

```python
# Python 2:
import urllib2
response = urllib2.urlopen('http://example.com')

import urllib
urllib.urlencode({'a': 1})

# Python 3:
import urllib.request
response = urllib.request.urlopen('http://example.com')

import urllib.parse
urllib.parse.urlencode({'a': 1})

# Better: just use requests in both
# pip install requests
import requests
r = requests.get('http://example.com')
```

### Other common removals

```python
# has_key() → in operator
d.has_key('foo')   # Python 2 only
'foo' in d         # Python 3 (works in both)

# reduce() moved to functools
reduce(f, lst)                   # Python 2 builtin
from functools import reduce
reduce(f, lst)                   # Python 3

# reload() moved to importlib
reload(module)                   # Python 2 builtin
from importlib import reload
reload(module)                   # Python 3

# execfile() removed
execfile('script.py')            # Python 2 only
exec(open('script.py').read())   # Python 3

# long type removed
x = 42L       # Python 2 only — just use int in Python 3

# cmp() removed
cmp(a, b)      # Python 2 only
(a > b) - (a < b)   # Python 3 equivalent
```

## Reading Python 2 Pickles in Python 3

```python
import pickle

# Python 2 pickles that contain str objects (bytes in Python 2)
with open('py2_data.pkl', 'rb') as f:
    data = pickle.load(f, encoding='latin1')   # str → str (most common fix)
    # or
    data = pickle.load(f, encoding='bytes')    # str → bytes

# If you get errors about ascii codec:
with open('py2_data.pkl', 'rb') as f:
    data = pickle.load(f, encoding='latin1')
```

## Reading Python 2 numpy / scipy files

```python
import numpy as np
import scipy.io

# .npy files from Python 2
arr = np.load('py2_array.npy', allow_pickle=True, encoding='latin1')

# .npz
npz = np.load('py2_data.npz', allow_pickle=True, encoding='latin1')

# .mat (MATLAB files saved from Python 2 scipy)
data = scipy.io.loadmat('data.mat')
```

## Identifying Python 2 Code Quickly

```bash
# Check for Python 2 syntax before running 2to3
python3 -m py_compile old_script.py   # SyntaxError = needs migration

# pylint can flag Python 2 patterns
pip install pylint
pylint --py3k old_script.py           # report Python 3 compatibility issues

# pyupgrade — upgrades old Python idioms even within Python 3 code
pip install pyupgrade
pyupgrade --py3-plus old_script.py
pyupgrade --py36-plus old_script.py   # target minimum version
```

## Common Patterns in Old Scientific Code

```python
# Old: string formatting
"Hello %s, you are %d years old" % (name, age)   # still works in Python 3
# Modern:
f"Hello {name}, you are {age} years old"

# Old: file I/O without encoding
f = open('data.txt')
# Fix (explicit encoding prevents UnicodeDecodeError):
f = open('data.txt', encoding='utf-8', errors='replace')

# Old: print to stderr
import sys
print >>sys.stderr, "error"
# Fix:
print("error", file=sys.stderr)

# Old: catching all exceptions
try:
    ...
except Exception, e:   # SyntaxError in Python 3
    ...
# Fix:
try:
    ...
except Exception as e:
    ...

# Old: integer keys in struct/array
import struct
fmt = 'I'
struct.pack(fmt, 42L)   # 42L is Python 2 long literal
# Fix:
struct.pack(fmt, 42)
```
