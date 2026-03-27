---
name: database-pro
description: Use for ANY database interaction, SQL generation, or data source management. Expert guide for PostgreSQL (queries/schemas), SQLAlchemy (ORM), Elasticsearch (search/indexing), and S3 (object storage). CRITICAL: Use `query-optimization` principles for all production queries.
---
# Database Pro (Consolidated)

Unified expert guide for high-performance data storage, retrieval, and optimization.

## ⚠️ Mandatory Pre-flight: Security & Performance

1. **Never Hardcode Credentials**: Always use environment variables or a secrets manager.
2. **Exhaustive Optimization**: For SQL queries, always check the execution plan (`EXPLAIN ANALYZE`) if latency exceeds 500ms.
3. **Resource Awareness**: Avoid `SELECT *` on tables with 100+ columns; select only what is needed.

---

## 1. PostgreSQL & SQL Mastering

Use for complex relational queries, schema design, and advanced analytics.

### Core Idioms
- **CTE First**: Use Common Table Expressions for complex, readable logic.
- **Window Functions**: Use `ROW_NUMBER()`, `RANK()`, and `LAG()/LEAD()` for analytical reporting.
- **Indexes**: Always index columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses.

```sql
-- Pattern for deduplicating data
WITH ranked_rows AS (
    SELECT id, created_at, 
           ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC) as rank
    FROM events
)
SELECT * FROM ranked_rows WHERE rank = 1;
```

---

## 2. SQLAlchemy (The Python Standard)

Use for database-agnostic access and ORM-based data modeling.

### Core Idioms
- **Declarative Base**: Use modern `mapped_column` syntax (SQLAlchemy 2.0+).
- **Session Management**: Always use context managers (`with Session() as session`) to prevent leaks.
- **Eager Loading**: Use `selectinload` or `joinedload` to avoid N+1 query problems.

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, select

class User(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)

# Query with Eager Loading
stmt = select(User).options(selectinload(User.orders)).where(User.id == 1)
```

---

## 3. Elasticsearch (Search & Analytics)

Use for full-text search, log aggregation, and real-time analytics.

### Core Tools
- **ES|QL**: Use the Piped Query Language for fast filtering and transformation.
- **Mappings**: Explicitly define field types (keyword vs text) to optimize search performance.

---

## 4. Object Storage (S3 & Compatible)

Use for large-scale unstructured data, data lakes, and model artifacts.

### Core Tool: `boto3`
- **Idiom**: Use `upload_file` for automatic multi-part uploads on large files.

```python
import boto3
s3 = boto3.client('s3')
s3.download_file('my-bucket', 'data/file.csv', 'local.csv')
```

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **SQL Injection**: Never use f-strings for SQL queries; use bound parameters.
2. **N+1 Queries**: Loading relationships in a loop instead of using `JOIN` or Eager Loading.
3. **Over-Indexing**: Adding indexes to every column slows down `INSERT` operations.
4. **Elasticsearch**: Treating ES as a primary relational database; it is a search engine.

## References
- `skills/data-sources/database-pro/references/postgresql/` — Advanced SQL and schema design.
- `skills/data-sources/database-pro/references/elasticsearch/` — ES|QL and mapping optimization.
- `skills/data-sources/database-pro/references/sqlalchemy/` — Migration and ORM patterns.
