---
name: parallel-processing-pro
description: Accelerates data tasks using Multithreading (I/O) and Multiprocessing (CPU). Use for parallel S3 downloads, batch API calls, and heavy numerical processing.
---
# Parallel Processing Pro

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
