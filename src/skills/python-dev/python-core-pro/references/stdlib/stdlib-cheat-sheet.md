# Python Standard Library - Advanced Cheat Sheet

## `pathlib` (FileSystem)

- `Path.cwd()` / `Path.home()`
- `p.exists()`, `p.is_file()`, `p.is_dir()`
- `p.mkdir(parents=True, exist_ok=True)`
- `p.unlink(missing_ok=True)` (delete file)
- `p.rmdir()` (delete empty dir)
- `p.rename(target)` / `p.replace(target)`
- `p.read_text()`, `p.write_text(data)`
- `p.owner()`, `p.group()`, `p.stat()`

## `collections` (Data Structures)

- `Counter(iterable).most_common(n)`
- `defaultdict(list)` (avoids `if key not in d: d[key] = []`)
- `deque(iterable, maxlen=N)` (circular buffer)
- `namedtuple('Point', ['x', 'y'])` (immutable)

## `itertools` (Iterators)

- `chain(*iterables)`: Flattening.
- `islice(iterable, start, stop, step)`: Slicing without memory overhead.
- `groupby(iterable, key)`: Grouping (must be sorted by key).
- `product(*iterables, repeat=1)`: Cartesian product.
- `permutations(p, r)` / `combinations(p, r)`.
- `zip_longest(*iterables, fillvalue=None)`.

## `functools` (Functions)

- `@lru_cache(maxsize=None)`: Memoization.
- `@wraps(func)`: Preserves metadata in decorators.
- `partial(func, *args, **keywords)`: Fixed-argument functions.
- `reduce(function, iterable)`: Cumulative calculation.

## `contextlib` (Context Managers)

- `@contextmanager`: Create CM from generator.
- `ExitStack()`: Manage multiple CMs dynamically.
- `suppress(*exceptions)`: Ignore specific errors.
- `closing(thing)`: Ensure `.close()` is called.

## `bisect` & `heapq` (Algos)

- `bisect.bisect_left(a, x)`: Index to maintain sort.
- `bisect.insort(a, x)`: Insert into sorted list.
- `heapq.heappush(h, item)` / `heapq.heappop(h)`.
- `heapq.nlargest(n, iterable)` / `heapq.nsmallest(n, iterable)`.

## `shutil` (High-level File Ops)

- `shutil.copy2(src, dst)`: Copy file + metadata.
- `shutil.copytree(src, dst)`: Recursive copy.
- `shutil.rmtree(path)`: Recursive delete.
- `shutil.move(src, dst)`: Recursive move.
- `shutil.disk_usage(path)`.
- `shutil.which(cmd)`: Find executable.

## `tempfile` (Temporary Storage)

- `tempfile.TemporaryFile()`: Auto-deleted file.
- `tempfile.NamedTemporaryFile()`: Has a path on disk.
- `tempfile.TemporaryDirectory()`: Auto-deleted directory.

## `json` (Serialization)

- `json.dumps(obj, indent=4, sort_keys=True)`
- `json.loads(s)`
- `json.dump(obj, fp)` / `json.load(fp)`
- Custom `JSONEncoder`:

```python
import json
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)
```
