---
name: numpy
description: Performs numerical computing and vectorized math using arrays. Use for fast array manipulation, binary data buffers, and linear algebra. CRITICAL: Run `get-available-resources` for arrays > 10^7 elements to prevent OOM.
---
# NumPy

## ⚠️ Mandatory Pre-flight: Resource Check

Numerical arrays can consume significant RAM (e.g., a `float64` array of 10^9 elements uses ~8GB).

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Strategy**:
   - **Large Arrays**: If array size > 25% of available RAM, prefer `memmap` or switch to `dask.array`.
   - **Dtype Optimization**: Use `float32` instead of `float64` to halve memory if extreme precision is not required.

## Reproducibility & Randomness (MANDATORY)

Never use the legacy `np.random.*` functions. Always use the modern `Generator` API with a fixed seed.

```python
import numpy as np
RANDOM_STATE = 42

# Modern API (Thread-safe and reproducible)
rng = np.random.default_rng(seed=RANDOM_STATE)
arr = rng.standard_normal((100, 100))
```

## Common Pitfalls (The "Wall of Shame")

1. **Python Loops**: Using `for x in arr:` is 100x slower than vectorized `np.sin(arr)`.
2. **Implicit Copies**: Functions like `flatten()` or "fancy indexing" (`arr[[1, 2]]`) create copies. Use `ravel()` or slicing for views.
3. **Array Concatenation in Loops**: `np.append` or `np.concatenate` in a loop is $O(N^2)$. Pre-allocate with `np.empty()` and fill.

## Array Creation

```python
import numpy as np

# From Python
np.array([1, 2, 3])
np.array([[1, 2], [3, 4]], dtype=np.float32)

# Ranges
np.arange(0, 10, 2)                  # [0, 2, 4, 6, 8]
np.linspace(0, 1, 50)                # 50 evenly spaced points
np.logspace(0, 3, 10)                # 10 points from 10^0 to 10^3

# Filled
np.zeros((3, 4))
np.ones((3, 4), dtype=np.int16)
np.full((3, 4), fill_value=np.nan)
np.eye(4)                            # identity matrix
np.empty((1000,), dtype=np.float64)  # uninitialized (fastest)

# From existing
np.zeros_like(arr)
np.ones_like(arr)
np.full_like(arr, 99)

# Random
rng = np.random.default_rng(seed=42)  # modern API (prefer over np.random.*)
rng.random((3, 4))                     # uniform [0, 1)
rng.integers(0, 100, size=(3, 4))
rng.normal(loc=0, scale=1, size=1000)
rng.choice(arr, size=10, replace=False)
rng.shuffle(arr)                       # in-place
```

## dtypes

```python
# Integer
np.int8, np.int16, np.int32, np.int64
np.uint8, np.uint16, np.uint32, np.uint64

# Float
np.float16, np.float32, np.float64   # float64 = default
np.complex64, np.complex128

# Boolean, string, object
np.bool_
np.str_    # fixed-width unicode
np.bytes_  # fixed-width bytes

# Check / convert
arr.dtype
arr.astype(np.float32)               # copy with new dtype
arr.astype(np.float32, copy=False)   # avoid copy if already correct type

# Info
np.iinfo(np.int16)    # min=-32768, max=32767
np.finfo(np.float32)  # eps, min, max
```

## Indexing and Slicing

```python
a = np.arange(24).reshape(4, 6)

# Basic (returns views — no copy)
a[0]           # first row
a[:, 2]        # column 2
a[1:3, 2:5]    # submatrix
a[::2, ::2]    # every other row and column

# Integer array indexing (fancy indexing — returns copy)
a[[0, 2, 3]]            # rows 0, 2, 3
a[:, [1, 4]]            # columns 1 and 4
a[[0, 2], [1, 4]]       # elements (0,1) and (2,4)

# Boolean indexing (returns copy)
a[a > 10]               # flat array of values > 10
a[a % 2 == 0]           # even values
mask = (a > 5) & (a < 15)
a[mask] = 0             # in-place assignment via mask

# np.where — conditional selection
np.where(a > 10, a, 0)           # keep values > 10, else 0
np.where(a > 10, a, -a)          # positive where > 10, negated elsewhere
idx = np.where(a > 10)           # returns tuple of index arrays
rows, cols = np.where(a > 10)

# nonzero / argwhere
np.nonzero(a > 10)               # same as np.where with one condition
np.argwhere(a > 10)              # Nx2 array of (row, col) pairs
```

## Shape Manipulation

```python
a = np.arange(24)

a.reshape(4, 6)        # new shape (must be same total elements)
a.reshape(4, -1)       # -1 = infer dimension
a.reshape(-1, 6)

a.ravel()              # flatten to 1D (view if possible)
a.flatten()            # flatten to 1D (always copy)

a.T                    # transpose (view)
np.transpose(a, (1, 0, 2))   # reorder axes of 3D array

# Add/remove dimensions
a[:, np.newaxis]       # (n,) → (n, 1)
a[np.newaxis, :]       # (n,) → (1, n)
np.expand_dims(a, 0)
np.squeeze(a)          # remove size-1 dimensions

# Stack and split
np.stack([a, b], axis=0)     # new axis
np.vstack([a, b])             # vertical stack (rows)
np.hstack([a, b])             # horizontal stack (columns)
np.concatenate([a, b], axis=1)

np.split(a, 3)               # split into 3 equal parts
np.split(a, [2, 5])          # split at indices 2 and 5
np.array_split(a, 3)         # like split but allows unequal sizes
```

## Broadcasting

Broadcasting lets you operate on arrays of different shapes without copying:

```python
a = np.ones((3, 4))
b = np.array([1, 2, 3, 4])    # shape (4,)

a + b   # b is broadcast across rows → (3, 4)

# Rules: shapes are compared right-to-left
# (3, 4) + (4,)   → (3, 4)  ✓
# (3, 4) + (3, 1) → (3, 4)  ✓
# (3, 4) + (3,)   → ERROR    ✗ (align from right: 4 ≠ 3)

# Common patterns
col = np.array([[1], [2], [3]])    # (3, 1)
row = np.array([10, 20, 30, 40])   # (4,)
col + row   # → (3, 4)  outer sum

# Normalize rows (subtract row mean)
a - a.mean(axis=1, keepdims=True)

# Normalize columns (subtract column mean)
a - a.mean(axis=0)
```

## Math Operations

```python
# Element-wise (ufuncs — vectorized, fast)
np.add(a, b)         # same as a + b
np.subtract(a, b)
np.multiply(a, b)
np.divide(a, b)
np.power(a, 2)       # a ** 2
np.sqrt(a)
np.abs(a)
np.exp(a)
np.log(a)            # natural log
np.log2(a)
np.log10(a)
np.sin(a); np.cos(a); np.tan(a)
np.clip(a, 0, 100)   # clamp values

# Reductions
a.sum()              # total
a.sum(axis=0)        # sum along rows → column sums
a.sum(axis=1)        # sum along columns → row sums
a.mean(); a.std(); a.var()
a.min(); a.max()
a.argmin(); a.argmax()           # index of min/max
np.cumsum(a, axis=0)             # cumulative sum along axis

# Linear algebra
np.dot(a, b)         # dot product / matrix multiply
a @ b                # same, cleaner syntax
np.linalg.inv(a)
np.linalg.solve(A, b)
np.linalg.norm(a)
np.linalg.eig(a)
U, s, Vt = np.linalg.svd(a)

# Comparisons
np.allclose(a, b, rtol=1e-5)    # are all values close?
np.isnan(a).any()
np.isinf(a).any()
np.isfinite(a)
```

## Structured Arrays (like a typed table)

Structured arrays are the NumPy equivalent of a row-based binary record format:

```python
# Define dtype (field names and types)
dtype = np.dtype([
    ('timestamp', '<u8'),    # uint64, little-endian
    ('channel',   '<u2'),    # uint16
    ('value',     '<f4'),    # float32
    ('flags',     '<u1'),    # uint8
])

# Create
arr = np.zeros(100, dtype=dtype)
arr['timestamp'] = np.arange(100)
arr['value'] = np.random.rand(100)

# Access by field name
arr['value']          # array of float32
arr[0]                # single record
arr[0]['timestamp']   # single field of single record

# Load from binary file (fastest way to read fixed-width binary data)
with open('data.bin', 'rb') as f:
    f.seek(header_size)
    arr = np.frombuffer(f.read(), dtype=dtype)

# → pandas DataFrame
import pandas as pd
df = pd.DataFrame(arr)
```

## Views vs Copies

Understanding this prevents subtle bugs:

```python
a = np.arange(10)

# Views (no memory copy — modifying changes original)
b = a[2:5]        # slice → view
b = a.reshape(2, 5)
b = a.T
b = a.view(np.float32)   # reinterpret bytes

# Copies (independent)
b = a[[0, 2, 4]]  # fancy indexing → copy
b = a[a > 5]      # boolean indexing → copy
b = a.copy()      # explicit copy
b = a.flatten()   # always copy

# Check
np.shares_memory(a, b)  # True if they share memory
b.base is a             # True if b is a view of a
```

## Performance Tips

```python
# Use views instead of copies where possible
arr[::2]          # view, no copy
arr[arr > 0]      # copy (unavoidable for boolean index)

# Pre-allocate output arrays
out = np.empty(n, dtype=np.float64)
np.add(a, b, out=out)        # write result into pre-allocated array

# Avoid Python loops — use vectorized ufuncs
# BAD:
result = [np.sin(x) for x in arr]
# GOOD:
result = np.sin(arr)

# Use appropriate dtype (smaller = faster cache usage)
arr.astype(np.float32)   # half the memory of float64

# contiguous memory layout matters for cache performance
arr = np.ascontiguousarray(arr)   # C-order (row-major)
arr = np.asfortranarray(arr)      # Fortran-order (column-major)
arr.flags['C_CONTIGUOUS']

# np.einsum for complex tensor operations (often faster than explicit loops)
np.einsum('ij,jk->ik', A, B)     # matrix multiply
np.einsum('ij->i', A)            # row sum
np.einsum('ij,ij->i', A, B)      # row-wise dot product
```
