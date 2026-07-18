# Kùzu Domain Glossary

| Term | Definition | Source | Real Example |
|---|---|---|---|
| Node table | A table that stores graph vertices, each with a primary key and properties | Verified `CREATE NODE TABLE` probe | `CREATE NODE TABLE User(name STRING PRIMARY KEY, age INT64)` |
| Relationship table (rel table) | A table that stores directed edges between node tables, optionally with properties | Verified `CREATE REL TABLE` probe | `CREATE REL TABLE Follows(FROM User TO User, since INT64)` |
| Primary key | Exactly one column per node table that uniquely identifies nodes | API behavior | `name STRING PRIMARY KEY` |
| Node label | The table name used in Cypher patterns | Cypher query | `(u:User)` |
| Relationship type | The rel-table name used in Cypher patterns | Cypher query | `[:Follows]` |
| Variable-length / recursive path | A pattern that traverses a relationship 1 to N hops | Verified query output | `(a:User)-[:Follows*1..3]->(b:User)` |
| COPY FROM | Bulk-load statement for CSV or Parquet files | Verified load probe | `COPY User FROM "user.csv" (header=true)` |
| Prepared statement / parameters | Passing values separately from the query text | API deprecation warning + verified probe | `conn.execute("... $name ...", {"name": "Bob"})` |
| Embedded database | Database runs inside the application process, no server | Package behavior | `kuzu.Database("demo_db")` |
