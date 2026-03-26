# Oracle Database Reference (`python-oracledb`)

## Quick Start
```python
import oracledb

# Thin mode (No client required)
con = oracledb.connect(user='u', password='p', dsn='host:1521/SVC')

with con.cursor() as cur:
    cur.execute("SELECT * FROM t WHERE id = :id", id=42)
    row = cur.fetchone()
```

## Dialect Tips
- **Bind Variables**: Always use `:name` or `:1`.
- **Pagination**: Use `OFFSET :n ROWS FETCH NEXT :m ROWS ONLY`.
- **Merge**: Use `MERGE INTO ...` for upserts.
