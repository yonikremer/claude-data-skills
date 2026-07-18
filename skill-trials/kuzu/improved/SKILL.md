---
name: kuzu-graph-db
description: Use when you need to create, load, or query an embedded property-graph database using Kùzu and its Cypher-like query language.
---

# Kùzu Graph Database

## Mandatory Pre-flight

- Install the package: `pip install kuzu`.
- Kùzu is an **embedded** database (no separate server process). The database path is a file prefix on disk.
- Import the Python module: `import kuzu`.

## Domain Fundamentals

Kùzu is a property graph database. Unlike relational tables, you model data as:

- **Nodes**: entities with properties and a primary key. Declared in a **node table**.
- **Relationships**: typed, directed edges between nodes. Declared in a **relationship table** (rel table).
- **Labels**: Kùzu uses table names as node/relationship labels in Cypher `MATCH` patterns.
- **Cypher**: a declarative graph query language. Kùzu supports a subset that includes `MATCH`, `CREATE`, `COPY FROM`,
  variable-length (recursive) patterns, and parameters.

## Minimal Example

```python
import kuzu

db = kuzu.Database("demo_db")
conn = kuzu.Connection(db)

conn.execute("CREATE NODE TABLE User(name STRING PRIMARY KEY, age INT64)")
conn.execute('CREATE REL TABLE Follows(FROM User TO User, since INT64)')
conn.execute('COPY User FROM "user.csv" (header=true)')
conn.execute('COPY Follows FROM "follows.csv" (header=true)')

result = conn.execute("MATCH (u:User) WHERE u.age > 25 RETURN u.name")
while result.has_next():
    print(result.get_next())
```

## Idiomatic Example: Recursive Query + Parameters

```python
import kuzu

db = kuzu.Database("demo_db")
conn = kuzu.Connection(db)

# Find everyone reachable within 1-3 hops of "Alice"
result = conn.execute(
    "MATCH (a:User)-[:Follows*1..3]->(b:User) WHERE a.name = $name RETURN b.name",
    {"name": "Alice"},
)
while result.has_next():
    print(result.get_next())
```

## Key DDL/DML Patterns

| Task | Query |
|---|---|
| Create node table | `CREATE NODE TABLE User(name STRING PRIMARY KEY, age INT64)` |
| Create rel table | `CREATE REL TABLE Follows(FROM User TO User, since INT64)` |
| Bulk load nodes | `COPY User FROM "user.csv" (header=true)` |
| Bulk load edges | `COPY Follows FROM "follows.csv" (header=true)` |
| List tables | `CALL show_tables() RETURN *` |
| Variable-length path | `MATCH (a)-[:Follows*1..3]->(b)` |
| Parameterized query | `conn.execute("... WHERE u.name = $name RETURN u.age", {"name": "Bob"})` |

## Wall of Shame

- **Database path is a file prefix, not a directory.** Use `kuzu.Database("path/to/db")`; Kùzu will create files around it.
- **No multi-column primary keys.** A node table can have exactly one primary key column.
- **Relationship tables have fixed direction and endpoint labels.** `FROM User TO User` means you cannot later use `Follows` between `User` and `City`.
- **Prepared-statement API is deprecated.** Do not call `conn.prepare(...)`. Pass parameters directly to `conn.execute(query, params)`.
- **`COPY FROM` uses double-quoted file paths**, not single-quoted strings.
- **`conn.query()` does not exist.** Use `conn.execute(...)` for both DDL and read queries.

## Reference Pointers

- Schema reference and verified examples: `references/tech-specs.md`
- Domain terminology: `references/glossary.md`
