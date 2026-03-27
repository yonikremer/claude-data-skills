# PostgreSQL Reference (`psycopg2`)

## Quick Start
```python
import psycopg2
from psycopg2.extras import execute_values

con = psycopg2.connect(dsn="postgresql://user:pass@host:5432/db")

# execute_values is the Gold Standard for bulk inserts
with con.cursor() as cur:
    execute_values(cur, "INSERT INTO t (a, b) VALUES %s", rows)
con.commit()
```

## Performance: COPY
The `COPY` command is significantly faster than `INSERT` for large datasets.
```python
import io
buf = io.StringIO()
df.to_csv(buf, index=False, header=False)
buf.seek(0)
with con.cursor() as cur:
    cur.copy_from(buf, 'table_name', sep=',')
```

## JSONB
Postgres supports advanced JSON indexing.
- Access: `data->>'field'`
- Search: `data @> '{"key": "value"}'`
