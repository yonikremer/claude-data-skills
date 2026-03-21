---
name: postgresql
description: Connects to and manages PostgreSQL databases for production data. Use when performing complex queries, transactions, or bulk loading with COPY. Do NOT use for simple local storage (use sqlite) or for database-agnostic code (use sqlalchemy).
---
# PostgreSQL

## Quick Start

```python
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# --- psycopg2 (raw driver) ---
con = psycopg2.connect(
    host='localhost', port=5432,
    dbname='mydb', user='myuser', password='secret'
)

# --- SQLAlchemy (for pandas integration) ---
engine = create_engine('postgresql+psycopg2://myuser:secret@localhost:5432/mydb')

# Query into pandas
df = pd.read_sql('SELECT * FROM my_table WHERE val > 100', engine)

# Write DataFrame to table
df.to_sql('my_table', engine, if_exists='append', index=False, method='multi')
```

## Connection String Formats

```python
# psycopg2
psycopg2.connect("host=localhost port=5432 dbname=mydb user=myuser password=secret")
psycopg2.connect(dsn="postgresql://myuser:secret@localhost:5432/mydb")

# SQLAlchemy
create_engine('postgresql+psycopg2://user:pass@host:5432/db')
create_engine('postgresql+psycopg2://user:pass@host:5432/db?sslmode=require')

# From environment variable (recommended for security)
import os
create_engine(os.environ['DATABASE_URL'])

# Connection pool tuning
create_engine(url, pool_size=5, max_overflow=10, pool_timeout=30,
              pool_pre_ping=True)  # test connections before use
```

## Querying with psycopg2

```python
import psycopg2.extras

con = psycopg2.connect(dsn='...')

# Always use %s placeholders — NEVER string-format SQL (SQL injection risk)
with con.cursor() as cur:
    cur.execute("SELECT * FROM t WHERE id = %s AND status = %s", (42, 'active'))
    rows = cur.fetchall()
    columns = [d[0] for d in cur.description]

# DictCursor — rows as dicts
with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
    cur.execute("SELECT id, val FROM t WHERE id = %s", (42,))
    row = cur.fetchone()
    print(row['val'])

# RealDictCursor — true dicts
with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    cur.execute("SELECT * FROM t")
    rows = cur.fetchall()   # list of dicts

# NamedTupleCursor
with con.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
    cur.execute("SELECT id, val FROM t")
    for row in cur:
        print(row.id, row.val)
```

## Writes and Transactions

```python
# Single insert
with con.cursor() as cur:
    cur.execute(
        "INSERT INTO measurements (ts, channel, val) VALUES (%s, %s, %s)",
        ('2024-01-01', 1, 3.14)
    )
con.commit()

# executemany (moderate speed)
rows = [(i, f'val_{i}') for i in range(1000)]
with con.cursor() as cur:
    cur.executemany("INSERT INTO t (a, b) VALUES (%s, %s)", rows)
con.commit()

# execute_values (fast bulk insert — recommended)
from psycopg2.extras import execute_values
with con.cursor() as cur:
    execute_values(cur,
        "INSERT INTO t (a, b) VALUES %s",
        rows,
        page_size=1000
    )
con.commit()

# Upsert (INSERT ... ON CONFLICT)
with con.cursor() as cur:
    execute_values(cur, """
        INSERT INTO t (id, val) VALUES %s
        ON CONFLICT (id) DO UPDATE SET val = EXCLUDED.val
    """, rows)
con.commit()

# Rollback on error
try:
    with con.cursor() as cur:
        cur.execute("UPDATE ...")
    con.commit()
except Exception:
    con.rollback()
    raise
```

## COPY — Fastest Bulk I/O

```python
import io, csv

# COPY FROM (bulk insert — orders of magnitude faster than INSERT)
with con.cursor() as cur:
    buf = io.StringIO()
    writer = csv.writer(buf)
    for row in data:
        writer.writerow(row)
    buf.seek(0)
    cur.copy_from(buf, 'my_table', sep=',', columns=('col_a', 'col_b'))
con.commit()

# From DataFrame via COPY
def df_to_pg_copy(df: pd.DataFrame, table: str, con):
    buf = io.StringIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)
    with con.cursor() as cur:
        cur.copy_from(buf, table, sep=',', null='',
                      columns=list(df.columns))
    con.commit()

# COPY TO (bulk export)
with con.cursor() as cur:
    with open('export.csv', 'w') as f:
        cur.copy_expert("COPY my_table TO STDOUT WITH CSV HEADER", f)
```

## pandas Integration

```python
from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine('postgresql+psycopg2://user:pass@host:5432/db',
                       pool_pre_ping=True)

# Read
df = pd.read_sql('SELECT * FROM my_table', engine)
df = pd.read_sql(text("SELECT * FROM t WHERE id = :id"), engine, params={'id': 42})
df = pd.read_sql('SELECT * FROM t', engine, parse_dates=['created_at'])

# Write (use method='multi' or 'copy' for speed)
df.to_sql('my_table', engine, if_exists='append',  index=False, method='multi')
df.to_sql('my_table', engine, if_exists='replace', index=False, chunksize=10_000)

# Chunked read for large tables
for chunk in pd.read_sql('SELECT * FROM big_table', engine, chunksize=50_000):
    process(chunk)
```

## Schema Inspection

```python
# List tables
pd.read_sql("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
""", engine)

# Column info
pd.read_sql("""
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_name = 'my_table'
    ORDER BY ordinal_position
""", engine)

# Table sizes
pd.read_sql("""
    SELECT relname AS table,
           pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
           n_live_tup AS row_estimate
    FROM pg_stat_user_tables
    ORDER BY pg_total_relation_size(relid) DESC
""", engine)

# Running queries
pd.read_sql("""
    SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
    FROM pg_stat_activity
    WHERE state != 'idle'
""", engine)
```

## Common Patterns

```python
# Parameterized IN clause
ids = [1, 2, 3, 4]
df = pd.read_sql(
    'SELECT * FROM t WHERE id = ANY(%s)',
    con, params=(ids,)
)
# or with SQLAlchemy:
df = pd.read_sql(
    text('SELECT * FROM t WHERE id = ANY(:ids)'),
    engine, params={'ids': ids}
)

# Temp table for complex multi-step queries
with engine.connect() as conn:
    conn.execute(text("CREATE TEMP TABLE tmp AS SELECT ..."))
    df = pd.read_sql('SELECT * FROM tmp JOIN other ON ...', conn)

# JSON columns
df = pd.read_sql("SELECT id, data->>'field' AS field FROM t", engine)
df = pd.read_sql("SELECT id, jsonb_array_elements(items) AS item FROM t", engine)
```
