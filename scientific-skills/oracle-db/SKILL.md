---
name: oracle-db
description: Connect to Oracle Database from Python using python-oracledb (thin mode, no Oracle Client needed) or cx_Oracle (thick mode). Use for querying Oracle production databases, bulk data extraction into pandas, and DDL/DML operations. Covers TNS/Easy Connect strings, LOBs, DATE/TIMESTAMP types, ROWNUM pagination, and pandas integration.
license: https://www.oracle.com/database/
metadata:
    skill-author: K-Dense Inc.
---

# Oracle Database

## Overview

Two Oracle Python drivers:
- **`python-oracledb`** (recommended) — pure Python, no Oracle Client install required (thin mode). Successor to cx_Oracle.
- **`cx_Oracle`** — requires Oracle Instant Client. Use when thick-mode features are needed (advanced queuing, DRCP, etc.).

```bash
pip install python-oracledb   # recommended
# or
pip install cx_Oracle         # legacy; requires Oracle Instant Client
```

## Quick Start

```python
import oracledb
import pandas as pd

# Thin mode (no Oracle Client needed)
con = oracledb.connect(
    user='myuser',
    password='secret',
    dsn='hostname:1521/SERVICE_NAME'  # Easy Connect format
)

# Query
with con.cursor() as cur:
    cur.execute("SELECT id, val FROM my_table WHERE id = :id", id=42)
    rows = cur.fetchall()

# pandas
df = pd.read_sql("SELECT * FROM my_table WHERE ROWNUM <= 1000", con)
con.close()
```

## Connection Formats

```python
import oracledb

# Easy Connect (host:port/service)
con = oracledb.connect(user='u', password='p', dsn='host:1521/MYSERVICE')

# TNS alias (requires tnsnames.ora)
con = oracledb.connect(user='u', password='p', dsn='MYALIAS')

# Full connection string
con = oracledb.connect(
    user='u', password='p',
    dsn='(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=host)(PORT=1521))'
        '(CONNECT_DATA=(SERVICE_NAME=MYSERVICE)))'
)

# Connection pool (for multi-threaded apps)
pool = oracledb.create_pool(
    user='u', password='p', dsn='host:1521/SVC',
    min=2, max=10, increment=1
)
with pool.acquire() as con:
    df = pd.read_sql("SELECT ...", con)

# SQLAlchemy URL
from sqlalchemy import create_engine
engine = create_engine('oracle+oracledb://user:pass@host:1521/?service_name=SVC')
# cx_Oracle variant:
engine = create_engine('oracle+cx_oracle://user:pass@host:1521/?service_name=SVC')
```

## Querying

```python
# Named bind variables (:name) — preferred
with con.cursor() as cur:
    cur.execute("""
        SELECT id, name, value
        FROM my_table
        WHERE status = :status AND created_date >= :dt
    """, status='ACTIVE', dt='2024-01-01')
    # or dict form:
    cur.execute("...", {'status': 'ACTIVE', 'dt': '2024-01-01'})

# Positional bind variables (:1, :2)
cur.execute("SELECT * FROM t WHERE id = :1 AND name = :2", (42, 'foo'))

# Fetch options
row  = cur.fetchone()       # one row as tuple
rows = cur.fetchall()
rows = cur.fetchmany(1000)

# Iterate (memory-efficient for large result sets)
cur.execute("SELECT * FROM big_table")
for row in cur:
    process(row)

# Column names
columns = [col[0] for col in cur.description]
```

## Oracle-Specific SQL Patterns

```python
# Pagination (Oracle 12c+ supports FETCH FIRST / OFFSET)
cur.execute("""
    SELECT * FROM my_table
    ORDER BY id
    OFFSET :offset ROWS FETCH NEXT :n ROWS ONLY
""", offset=100, n=50)

# Older Oracle pagination with ROWNUM
cur.execute("""
    SELECT * FROM (
        SELECT t.*, ROWNUM rn FROM my_table t WHERE ROWNUM <= :max_row
    ) WHERE rn > :min_row
""", max_row=200, min_row=100)

# SYSDATE / SYSTIMESTAMP
cur.execute("SELECT * FROM t WHERE created_date >= SYSDATE - INTERVAL '7' DAY")
cur.execute("SELECT SYSDATE FROM DUAL")   # test connection

# Sequence
cur.execute("SELECT my_seq.NEXTVAL FROM DUAL")

# MERGE (upsert)
cur.execute("""
    MERGE INTO target t
    USING (SELECT :id AS id, :val AS val FROM DUAL) s
    ON (t.id = s.id)
    WHEN MATCHED THEN UPDATE SET t.val = s.val
    WHEN NOT MATCHED THEN INSERT (id, val) VALUES (s.id, s.val)
""", id=42, val=3.14)
```

## Bulk Operations

```python
# executemany — fast bulk insert
rows = [(i, f'val_{i}') for i in range(10_000)]
with con.cursor() as cur:
    cur.executemany("INSERT INTO t (id, val) VALUES (:1, :2)", rows)
con.commit()

# Batch errors (continue on row-level errors)
with con.cursor() as cur:
    cur.executemany("INSERT INTO t VALUES (:1, :2)", rows,
                    batcherrors=True, arraydmlrowcounts=True)
    errors = cur.getbatcherrors()
    for err in errors:
        print(f"Row {err.offset}: {err.message}")
con.commit()
```

## Date and Timestamp Types

Oracle DATE includes time; Python receives `datetime.datetime`:

```python
import datetime

cur.execute("SELECT created_date FROM t WHERE id = :1", (42,))
row = cur.fetchone()
dt = row[0]   # datetime.datetime object

# Insert datetime
cur.execute("INSERT INTO t (id, ts) VALUES (:1, :2)",
            (1, datetime.datetime(2024, 1, 15, 10, 30, 0)))

# Oracle TIMESTAMP WITH TIME ZONE → Python datetime with tzinfo
cur.execute("SELECT ts_tz FROM t")
```

## pandas Integration

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('oracle+oracledb://user:pass@host:1521/?service_name=SVC')

# Read
df = pd.read_sql('SELECT * FROM my_table WHERE ROWNUM <= 100000', engine)
df = pd.read_sql("""
    SELECT id, val, created_date
    FROM my_table
    WHERE status = 'ACTIVE'
""", engine, parse_dates=['created_date'])

# Chunked read
for chunk in pd.read_sql('SELECT * FROM big_table', engine, chunksize=50_000):
    process(chunk)

# Write
df.to_sql('my_table', engine, if_exists='append', index=False, method='multi')
```

## Schema Inspection

```python
# Tables owned by current user
pd.read_sql("SELECT table_name FROM user_tables ORDER BY table_name", engine)

# All accessible tables
pd.read_sql("SELECT owner, table_name FROM all_tables ORDER BY owner, table_name", engine)

# Column info
pd.read_sql("""
    SELECT column_name, data_type, data_length, nullable, data_default
    FROM user_tab_columns
    WHERE table_name = 'MY_TABLE'
    ORDER BY column_id
""", engine)

# Table row count estimates
pd.read_sql("""
    SELECT table_name, num_rows, last_analyzed
    FROM user_tables
    ORDER BY num_rows DESC NULLS LAST
""", engine)
```
