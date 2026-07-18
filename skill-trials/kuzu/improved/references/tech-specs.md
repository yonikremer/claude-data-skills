# Kùzu Technical Reference

## Source of truth

- Package: `kuzu` on PyPI (verified installed: `kuzu==0.11.3`)
- Docs site: `https://docs.kuzudb.com/` (network-unstable during validation; facts verified by running the package)

## Installation

```bash
pip install kuzu
```

## Architecture

- Embedded, in-process database.
- Database path is a file prefix; Kùzu creates the actual files on disk.
- Python API: `kuzu.Database(path)` + `kuzu.Connection(db)`.

## Verified DDL/DML

| Operation | Verified? | Command / API |
|---|---|---|
| Create node table | ✅ | `CREATE NODE TABLE User(name STRING PRIMARY KEY, age INT64)` |
| Create rel table | ✅ | `CREATE REL TABLE Follows(FROM User TO User, since INT64)` |
| Bulk copy nodes from CSV | ✅ | `COPY User FROM "user.csv" (header=true)` |
| Bulk copy rels from CSV | ✅ | `COPY Follows FROM "follows.csv" (header=true)` |
| List tables | ✅ | `CALL show_tables() RETURN *` |
| Recursive path | ✅ | `MATCH (a:User)-[:Follows*1..3]->(b:User)` |
| Parameterized query | ✅ | `conn.execute("...", {"name": "Bob"})` |

## Sample `show_tables()` output

```
[0, 'User', 'NODE', 'local(kuzu)', '']
[3, 'Follows', 'REL', 'local(kuzu)', '']
```

## Common data types

- `STRING`
- `INT64`
- `FLOAT`, `DOUBLE`
- `BOOLEAN`
- `DATE`, `TIMESTAMP`
- `BLOB`

Check the latest docs for the full list; prefer running `CREATE` against the installed version to verify type names.

## Coverage notes

The following public features are known from the docs but were **not probed** during validation. They are listed so a
future agent knows the full surface exists:

| Feature | Status | Note |
|---|---|---|
| `COPY ... TO "file.csv"` | UNVERIFIED | Export query results to CSV/Parquet |
| `EXPLAIN` | UNVERIFIED | Query plan output |
| `CALL show_connection() RETURN *` | UNVERIFIED | Connection/catalog introspection |
| Composite data types (ARRAY, STRUCT, MAP, UNION) | UNVERIFIED | Check installed version |
| RDF graph extensions | UNVERIFIED | Separate RDF support in some versions |
| Attaching external databases (DuckDB/PostgreSQL) | UNVERIFIED | Extension feature |

The skill intentionally covers the most common DDL/DML/query path; expand this matrix as more features are exercised.
