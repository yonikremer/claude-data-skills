---
name: sqlite
description: Manages embedded SQL databases for local storage and lightweight ETL. Use for prototyping SQL logic or local data management without a server. Do NOT use for production-scale relational data (use postgresql).
---
# SQLite

## Overview

SQLite is a serverless, file-based SQL database built into Python's standard library via `sqlite3`. It supports the full SQL query language and is ideal for local data storage, prototyping, and small-to-medium datasets.

## Quick Start

```python
import sqlite3
import pandas as pd

# Connect (creates file if it doesn't exist; ':memory:' for in-memory)
con = sqlite3.connect('mydata.db')

# Create table and insert
con.execute('''
    CREATE TABLE IF NOT EXISTS measurements (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        channel   INTEGER,
        value     REAL
    )
''')
con.execute("INSERT INTO measurements (timestamp, channel, value) VALUES (?, ?, ?)",
            ('2024-01-01 10:00:00', 1, 3.14))
con.commit()

# Query into pandas
df = pd.read_sql('SELECT * FROM measurements WHERE channel = 1', con)

# Bulk insert from DataFrame
df.to_sql('measurements', con, if_exists='append', index=False)

con.close()
```

## Connection Management

```python
# Context manager — commits on success, rolls back on exception
with sqlite3.connect('mydata.db') as con:
    con.execute("INSERT INTO t VALUES (?, ?)", (1, 'hello'))
    # auto-commit on __exit__

# Row factory — rows as dicts instead of tuples
con = sqlite3.connect('mydata.db')
con.row_factory = sqlite3.Row     # access columns by name: row['value']
# or
con.row_factory = lambda cur, row: dict(zip([c[0] for c in cur.description], row))

# Useful pragmas
con.execute('PRAGMA journal_mode=WAL')      # better concurrent read performance
con.execute('PRAGMA synchronous=NORMAL')    # safer than OFF, faster than FULL
con.execute('PRAGMA foreign_keys=ON')
con.execute(f'PRAGMA cache_size={-64*1024}')  # 64 MB cache
```

## CRUD Operations

```python
# Insert one row
con.execute("INSERT INTO t (a, b) VALUES (?, ?)", (1, 'x'))

# Insert many rows (fast bulk insert)
rows = [(i, f'val_{i}') for i in range(10000)]
con.executemany("INSERT INTO t (a, b) VALUES (?, ?)", rows)

# Update
con.execute("UPDATE t SET b = ? WHERE a = ?", ('new_val', 1))

# Delete
con.execute("DELETE FROM t WHERE a > ?", (100,))

# Upsert (INSERT OR REPLACE)
con.execute("INSERT OR REPLACE INTO t (a, b) VALUES (?, ?)", (1, 'upserted'))

# Always commit after writes (or use context manager)
con.commit()
```

## Querying

```python
cur = con.execute("SELECT * FROM measurements WHERE value > ?", (2.0,))

# Fetch options
row   = cur.fetchone()     # one row as tuple (or None)
rows  = cur.fetchall()     # all rows as list of tuples
rows  = cur.fetchmany(100) # batch of 100

# Iterate (memory-efficient for large results)
for row in con.execute("SELECT * FROM big_table"):
    process(row)

# Named parameters (more readable)
con.execute("SELECT * FROM t WHERE a = :a AND b = :b", {'a': 1, 'b': 'x'})
```

## pandas Integration

```python
import pandas as pd

con = sqlite3.connect('mydata.db')

# Read query result into DataFrame
df = pd.read_sql('SELECT * FROM measurements', con)
df = pd.read_sql('SELECT * FROM measurements WHERE channel = ?', con, params=(1,))
df = pd.read_sql('SELECT * FROM measurements', con,
                 parse_dates=['timestamp'], index_col='id')

# Write DataFrame to table
df.to_sql('measurements', con, if_exists='replace', index=False)  # replace table
df.to_sql('measurements', con, if_exists='append',  index=False)  # add rows
df.to_sql('measurements', con, if_exists='fail',    index=False)  # error if exists

# Chunked read for large tables
chunks = pd.read_sql('SELECT * FROM big_table', con, chunksize=50_000)
df = pd.concat(chunks, ignore_index=True)
```

## Schema Inspection

```python
# List tables
pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", con)

# Table schema
pd.read_sql("PRAGMA table_info(measurements)", con)

# Indexes
pd.read_sql("PRAGMA index_list(measurements)", con)

# All objects
pd.read_sql("SELECT * FROM sqlite_master", con)
```

## Indexes and Performance

```python
# Create index
con.execute("CREATE INDEX IF NOT EXISTS idx_channel ON measurements(channel)")
con.execute("CREATE INDEX IF NOT EXISTS idx_ts_chan ON measurements(timestamp, channel)")

# Analyze query plan
con.execute("EXPLAIN QUERY PLAN SELECT * FROM measurements WHERE channel = 1").fetchall()

# Vacuum (reclaim space after large deletes)
con.execute("VACUUM")

# Analyze (update statistics for query planner)
con.execute("ANALYZE")
```

## SQLAlchemy (use when you need ORM or cross-dialect compatibility)

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///mydata.db')
# engine = create_engine('sqlite://')  # in-memory

df = pd.read_sql('SELECT * FROM measurements', engine)
df.to_sql('measurements', engine, if_exists='append', index=False)

# Raw connection for non-pandas work
with engine.connect() as conn:
    result = conn.execute(text("SELECT count(*) FROM measurements"))
    print(result.scalar())
```

## Common Patterns

```python
# Load CSV into SQLite for SQL querying
df = pd.read_csv('data.csv')
con = sqlite3.connect(':memory:')
df.to_sql('data', con, index=False)
result = pd.read_sql('''
    SELECT category, AVG(value) as avg_val
    FROM data
    GROUP BY category
    ORDER BY avg_val DESC
''', con)

# Attach multiple database files
con.execute("ATTACH DATABASE 'archive.db' AS archive")
pd.read_sql("SELECT * FROM main.measurements UNION ALL SELECT * FROM archive.measurements", con)
```
