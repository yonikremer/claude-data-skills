---
name: multithreading-io
description: Speed up I/O-bound Python work using threads — concurrent DB queries, parallel file reads, simultaneous API calls, and S3 downloads. Use ThreadPoolExecutor for CPU-light work that spends time waiting (network, disk, database). For CPU-bound work use multiprocessing instead. Covers ThreadPoolExecutor, asyncio+aiohttp, Queue-based pipelines, and thread-safe patterns.
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# Multithreading for I/O-Bound Work

## When to Use Threads

The GIL (Global Interpreter Lock) means threads can't run Python bytecode in parallel, **but they can overlap I/O waits**. Threads are the right tool when your bottleneck is:
- Network calls (REST APIs, database queries)
- File reads/writes (especially many small files)
- S3 / cloud storage operations
- Any `time.sleep()` or blocking wait

For CPU-bound work (data transformation, parsing, computation), use `multiprocessing` or `ProcessPoolExecutor` instead.

## ThreadPoolExecutor — The Standard Tool

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

# Submit many tasks and collect results in order
def fetch_url(url: str) -> dict:
    import requests
    return requests.get(url, timeout=10).json()

urls = ['https://api.example.com/item/1', 'https://api.example.com/item/2', ...]

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))
    # results is in same order as urls, blocks until all complete

# Submit and process as they complete (out of order, faster feedback)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}

    for future in as_completed(futures):
        url = futures[future]
        try:
            data = future.result()
            process(data)
        except Exception as e:
            print(f"Failed {url}: {e}")
```

## Common I/O Patterns

### Parallel DB queries (multiple databases or queries)

```python
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from sqlalchemy import create_engine, text

ENGINES = {
    'prod':    create_engine('postgresql://...'),
    'staging': create_engine('postgresql://...'),
    'archive': create_engine('sqlite:///archive.db'),
}

def query_db(name: str, engine, sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, engine)

sql = "SELECT date, SUM(value) as total FROM metrics GROUP BY date"

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(query_db, name, engine, sql): name
        for name, engine in ENGINES.items()
    }
    results = {}
    for future in as_completed(futures):
        name = futures[future]
        results[name] = future.result()

combined = pd.concat(results, names=['source']).reset_index(level=0)
```

### Parallel S3 downloads

```python
from concurrent.futures import ThreadPoolExecutor
import boto3
import pandas as pd
import io

s3 = boto3.client('s3')

def download_parquet(key: str, bucket: str) -> pd.DataFrame:
    buf = io.BytesIO()
    s3.download_fileobj(bucket, key, buf)
    buf.seek(0)
    return pd.read_parquet(buf)

keys = ['data/2024-01.parquet', 'data/2024-02.parquet', ...]

with ThreadPoolExecutor(max_workers=8) as executor:
    dfs = list(executor.map(lambda k: download_parquet(k, 'my-bucket'), keys))

df = pd.concat(dfs, ignore_index=True)
```

### Parallel API calls with rate limiting

```python
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import requests

# Semaphore limits concurrent requests (rate limiting)
semaphore = threading.Semaphore(5)   # max 5 simultaneous requests

def fetch_with_limit(item_id: int) -> dict:
    with semaphore:
        resp = requests.get(f'https://api.example.com/items/{item_id}', timeout=10)
        resp.raise_for_status()
        return resp.json()

ids = range(1000)
with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(fetch_with_limit, ids))
```

### Parallel file reads

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd

def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

paths = list(Path('data/').glob('*.csv'))

with ThreadPoolExecutor(max_workers=8) as executor:
    dfs = list(executor.map(read_csv, paths))

df = pd.concat(dfs, ignore_index=True)
```

## Producer-Consumer Pipeline with Queue

Use when data arrives continuously (stream) or when producing and consuming have different speeds:

```python
import threading
import queue
import time

def producer(q: queue.Queue, items):
    """Fetch items and put them in the queue."""
    for item in items:
        result = fetch(item)    # I/O wait
        q.put(result)
    q.put(None)   # sentinel to signal completion

def consumer(q: queue.Queue, results: list):
    """Process items from the queue."""
    while True:
        item = q.get()
        if item is None:
            break
        results.append(process(item))
        q.task_done()

q = queue.Queue(maxsize=100)   # buffer of 100 items max
results = []

prod = threading.Thread(target=producer, args=(q, my_items))
cons = threading.Thread(target=consumer, args=(q, results))

prod.start(); cons.start()
prod.join(); cons.join()
```

### Multi-producer, multi-consumer

```python
import threading, queue
from concurrent.futures import ThreadPoolExecutor

NUM_PRODUCERS = 4
NUM_CONSUMERS = 2
SENTINEL = object()

q = queue.Queue(maxsize=200)

def producer(batch):
    for item in batch:
        q.put(fetch(item))

def consumer(results):
    while True:
        item = q.get()
        if item is SENTINEL:
            q.put(SENTINEL)   # pass sentinel to next consumer
            break
        results.append(process(item))

results = []
batches = [items[i::NUM_PRODUCERS] for i in range(NUM_PRODUCERS)]

with ThreadPoolExecutor(max_workers=NUM_PRODUCERS + NUM_CONSUMERS) as ex:
    prod_futures = [ex.submit(producer, b) for b in batches]
    cons_futures = [ex.submit(consumer, results) for _ in range(NUM_CONSUMERS)]

    for f in prod_futures:
        f.result()          # wait for all producers
    q.put(SENTINEL)         # signal consumers to stop
    for f in cons_futures:
        f.result()
```

## Thread-Safe Patterns

```python
import threading

# Lock — mutual exclusion for shared state
lock = threading.Lock()
shared_list = []

def append_safe(item):
    with lock:
        shared_list.append(item)

# thread-local storage — each thread gets its own instance
# Important for DB connections (connections are NOT thread-safe)
thread_local = threading.local()

def get_connection():
    if not hasattr(thread_local, 'conn'):
        thread_local.conn = create_connection()
    return thread_local.conn

def query(sql):
    conn = get_connection()   # each thread has its own connection
    return conn.execute(sql).fetchall()

# Event — signal between threads
done_event = threading.Event()

def background_task():
    do_work()
    done_event.set()

t = threading.Thread(target=background_task)
t.start()
done_event.wait(timeout=30)   # wait up to 30s
```

## asyncio — For High-Concurrency I/O

Use asyncio when you need thousands of concurrent connections (threads have OS overhead):

```python
import asyncio
import aiohttp       # pip install aiohttp
import pandas as pd

async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as resp:
        return await resp.json()

async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Run from a script
results = asyncio.run(fetch_all(urls))

# Run from Jupyter (event loop already running)
results = await fetch_all(urls)   # use await directly in Jupyter cell
```

### Async with rate limiting

```python
import asyncio, aiohttp

async def fetch_limited(sem: asyncio.Semaphore, session, url: str) -> dict:
    async with sem:
        async with session.get(url) as resp:
            return await resp.json()

async def fetch_all(urls, max_concurrent=10):
    sem = asyncio.Semaphore(max_concurrent)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_limited(sem, session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

## Choosing the Right Approach

| Situation | Tool |
|-----------|------|
| 10–100 DB queries or file reads | `ThreadPoolExecutor` |
| Simple parallel API calls | `ThreadPoolExecutor` |
| Streaming / continuous data | `queue.Queue` pipeline |
| 1000+ simultaneous HTTP requests | `asyncio` + `aiohttp` |
| CPU-bound: parsing, computation | `ProcessPoolExecutor` (not threads) |
| pandas `.apply()` too slow | `ProcessPoolExecutor` or `polars` |
