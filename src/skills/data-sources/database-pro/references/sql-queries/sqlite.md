# SQLite Reference (Python `sqlite3`)

## Quick Start

```python
import sqlite3
import pandas as pd

with sqlite3.connect('mydata.db') as con:
    # Use Row factory for dict-like access
    con.row_factory = sqlite3.Row
    
    # Pragma for speed
    con.execute('PRAGMA journal_mode=WAL')
    
    # Query into pandas
    df = pd.read_sql('SELECT * FROM measurements', con)
```

## Advanced Patterns

- **Memory Databases**: `sqlite3.connect(':memory:')`
- **Upsert**: `INSERT OR REPLACE INTO table ...`
- **Pragmas**: `WAL` mode for concurrency, `synchronous=NORMAL` for speed.
- **Bulk**: `con.executemany("INSERT INTO t VALUES (?, ?)", rows)`
