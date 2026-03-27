---
name: parallel-processing-pro
description: Use when accelerating data tasks through Multithreading (I/O-bound) or Multiprocessing (CPU-bound). Ideal for parallel S3 downloads, batch API calls, and heavy numerical processing. CRITICAL: Understand the GIL and pick the right strategy for the bottleneck.
---
# Parallel Processing Pro

## ⚠️ Mandatory Pre-flight: Resource Check

Parallelizing a task can multiply memory and CPU usage by the number of workers.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Worker Selection**: 
   - **CPU-bound**: Set `max_workers = logical_cores - 1` to prevent system freezing.
   - **I/O-bound**: `max_workers` can be $2 \times$ or $4 \times$ `logical_cores` depending on latency.
3. **Shared Memory**: Be cautious with large datasets in `Multiprocessing`. Each worker may spawn a copy of the data, potentially causing an OOM.

## Common Pitfalls (The "Wall of Shame")

1. **Threading for Math**: Attempting to use `threading` or `ThreadPoolExecutor` for CPU-intensive tasks. The GIL ensures only one thread executes Python bytecode at a time.
2. **Over-parallelization**: Spawning hundreds of threads/processes for small tasks. The overhead of spawning and context switching often exceeds the time saved.
3. **Pickle Errors**: Passing non-picklable objects (like active database connections or open file handles) to a `ProcessPoolExecutor`.

## References (Load on demand)
- `references/api-reference.md` — Formal signatures for multiprocessing and concurrent.futures.

## 1. Choosing the Strategy

| Bottleneck | Strategy | Tool |
| :--- | :--- | :--- |
| **I/O Bound** (Network, S3, DB) | **Multithreading** | `ThreadPoolExecutor` |
| **CPU Bound** (Math, Parsing, ML) | **Multiprocessing** | `ProcessPoolExecutor`, `joblib` |

## 2. Multithreaded S3 Downloads (MANDATORY PATTERN)

When downloading many files from S3, always use a `ThreadPoolExecutor` to overlap network latency.

```python
import boto3
from concurrent.futures import ThreadPoolExecutor
import io

s3 = boto3.client('s3')

def download_one(key, bucket):
    buf = io.BytesIO()
    s3.download_fileobj(bucket, key, buf)
    return buf.getvalue()

keys = ["file1.dat", "file2.dat", ...]
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(lambda k: download_one(k, "my-bucket"), keys))
```

## 3. Multiprocessing with `joblib` (Numerical Work)

`joblib` is the Gold Standard for parallelizing Python loops in data science.

```python
from joblib import Parallel, delayed
import numpy as np

def heavy_computation(data):
    return np.exp(data).sum()

# n_jobs=-1 uses all available CPU cores
results = Parallel(n_jobs=-1)(delayed(heavy_computation)(d) for d in data_list)
```

## 4. Common Pitfalls
- **GIL (Global Interpreter Lock)**: Python threads cannot run CPU-intensive tasks in parallel. Use `multiprocessing` for math.
- **Serialization (Pickling)**: Functions passed to `ProcessPoolExecutor` must be picklable. Avoid passing large objects; load them inside the worker if possible.
- **Race Conditions**: Always use `threading.Lock()` when multiple threads write to the same shared object.
- **Over-parallelization**: Too many workers can lead to context-switching overhead. Rule of thumb: `workers = cpu_count` for CPU, `workers = 2 * cpu_count` for I/O.
