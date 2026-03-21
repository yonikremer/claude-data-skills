---
name: sqlalchemy
description: Use SQLAlchemy for database-agnostic Python database access — connection pooling, SQL expression language (Core), ORM, schema reflection, and migrations with Alembic. Use when you need to work across multiple databases (SQLite, PostgreSQL, Oracle) with a unified API, or when you need ORM models. For simple pandas-only SQL work, use the database-specific skills directly.
license: https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
---

# SQLAlchemy

## Overview

SQLAlchemy has two layers:
- **Core** — SQL expression language, connection management, no ORM. Best for data engineering and analytics work.
- **ORM** — maps Python classes to tables. Best for application development.

For data work, Core is usually sufficient and more predictable.

```bash
pip install sqlalchemy
pip install psycopg2-binary   # for PostgreSQL
pip install oracledb           # for Oracle
# sqlite3 is in stdlib
```

## Connection URLs

```python
from sqlalchemy import create_engine

# SQLite
engine = create_engine('sqlite:///mydata.db')
engine = create_engine('sqlite://')                  # in-memory

# PostgreSQL
engine = create_engine('postgresql+psycopg2://user:pass@host:5432/db')
engine = create_engine('postgresql+psycopg2://user:pass@host:5432/db?sslmode=require')

# Oracle
engine = create_engine('oracle+oracledb://user:pass@host:1521/?service_name=SVC')

# Connection pool settings (important for production)
engine = create_engine(url,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,    # test connections before using them
    pool_recycle=3600,     # recycle connections after 1h
)
```

## Core — Raw SQL with Safety

```python
from sqlalchemy import create_engine, text

engine = create_engine('postgresql+psycopg2://...')

# Execute raw SQL safely with bound parameters
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM t WHERE id = :id AND status = :status"),
        {"id": 42, "status": "active"}
    )
    rows = result.fetchall()
    columns = result.keys()

    # Iterate (memory efficient)
    for row in result:
        print(row.id, row.value)    # attribute access by column name

    # Write — must commit explicitly
    conn.execute(text("INSERT INTO t (a, b) VALUES (:a, :b)"), {"a": 1, "b": "x"})
    conn.commit()

# Autocommit context
with engine.begin() as conn:    # auto-commits on success, rolls back on exception
    conn.execute(text("INSERT INTO t VALUES (:v)"), {"v": 42})
```

## Core — SQL Expression Language (type-safe, composable)

```python
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, DateTime, Boolean,
    select, insert, update, delete, and_, or_, func
)

engine = create_engine('sqlite:///mydata.db')
metadata = MetaData()

# Define table
measurements = Table('measurements', metadata,
    Column('id',        Integer, primary_key=True),
    Column('timestamp', DateTime),
    Column('channel',   Integer),
    Column('value',     Float),
    Column('status',    String(20)),
)

# Create table
metadata.create_all(engine)

# INSERT
with engine.begin() as conn:
    conn.execute(insert(measurements).values(channel=1, value=3.14, status='ok'))

# Bulk insert
with engine.begin() as conn:
    conn.execute(insert(measurements), [
        {'channel': 1, 'value': 3.14},
        {'channel': 2, 'value': 2.72},
    ])

# SELECT
stmt = (
    select(measurements)
    .where(and_(
        measurements.c.channel == 1,
        measurements.c.value > 0,
    ))
    .order_by(measurements.c.timestamp.desc())
    .limit(100)
)
with engine.connect() as conn:
    result = conn.execute(stmt)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

# Aggregation
stmt = (
    select(
        measurements.c.channel,
        func.avg(measurements.c.value).label('avg_val'),
        func.count().label('n'),
    )
    .group_by(measurements.c.channel)
    .having(func.count() > 10)
)

# UPDATE
with engine.begin() as conn:
    conn.execute(
        update(measurements)
        .where(measurements.c.status == 'pending')
        .values(status='processed')
    )

# DELETE
with engine.begin() as conn:
    conn.execute(delete(measurements).where(measurements.c.channel == 99))
```

## Schema Reflection (inspect existing database)

```python
from sqlalchemy import create_engine, inspect, MetaData, Table

engine = create_engine('postgresql+psycopg2://...')

# Inspect without defining tables
inspector = inspect(engine)

# List tables
inspector.get_table_names()
inspector.get_table_names(schema='myschema')

# Column info
inspector.get_columns('my_table')
# [{'name': 'id', 'type': INTEGER(), 'nullable': False, ...}, ...]

# Primary keys, foreign keys, indexes
inspector.get_pk_constraint('my_table')
inspector.get_foreign_keys('my_table')
inspector.get_indexes('my_table')

# Reflect table into Python object (for building queries dynamically)
metadata = MetaData()
my_table = Table('my_table', metadata, autoload_with=engine)
# Now use my_table.c.col_name in expressions
```

## ORM (when you need it)

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import String, Float, Integer

class Base(DeclarativeBase):
    pass

class Measurement(Base):
    __tablename__ = 'measurements'

    id:        Mapped[int]   = mapped_column(Integer, primary_key=True)
    channel:   Mapped[int]   = mapped_column(Integer, nullable=False)
    value:     Mapped[float] = mapped_column(Float)
    status:    Mapped[str]   = mapped_column(String(20), default='pending')

Base.metadata.create_all(engine)

# CRUD with ORM Session
with Session(engine) as session:
    # Insert
    m = Measurement(channel=1, value=3.14)
    session.add(m)
    session.commit()
    session.refresh(m)   # reload from DB (to get auto-generated id)
    print(m.id)

    # Query
    results = session.query(Measurement).filter(Measurement.channel == 1).all()

    # Modern style (SQLAlchemy 2.x)
    from sqlalchemy import select
    stmt = select(Measurement).where(Measurement.channel == 1).order_by(Measurement.value)
    results = session.scalars(stmt).all()

    # Update
    m = session.get(Measurement, 42)
    m.status = 'done'
    session.commit()

    # Delete
    session.delete(m)
    session.commit()
```

## pandas Integration

```python
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql+psycopg2://...')

# Read
df = pd.read_sql('SELECT * FROM my_table', engine)
df = pd.read_sql(text('SELECT * FROM t WHERE id = :id'), engine, params={'id': 42})
df = pd.read_sql_table('my_table', engine, schema='myschema')

# Write
df.to_sql('my_table', engine, if_exists='append', index=False, method='multi')
df.to_sql('my_table', engine, if_exists='replace', index=False, chunksize=10_000)

# Chunked read
for chunk in pd.read_sql('SELECT * FROM big_table', engine, chunksize=50_000):
    process(chunk)
```

## Alembic — Database Migrations

```bash
pip install alembic
alembic init alembic        # create alembic/ directory and alembic.ini
```

Edit `alembic/env.py` to point to your engine and metadata, then:

```bash
alembic revision --autogenerate -m "add status column"  # generate migration
alembic upgrade head                                      # apply all pending
alembic downgrade -1                                      # roll back one step
alembic current                                           # show current revision
alembic history                                           # list all revisions
```

Example migration file:

```python
# alembic/versions/abc123_add_status.py
def upgrade():
    op.add_column('measurements', sa.Column('status', sa.String(20), nullable=True))
    op.create_index('ix_measurements_status', 'measurements', ['status'])

def downgrade():
    op.drop_index('ix_measurements_status')
    op.drop_column('measurements', 'status')
```

## Connection Pool Monitoring

```python
from sqlalchemy import event

@event.listens_for(engine, "connect")
def on_connect(dbapi_conn, conn_record):
    print("New connection opened")

@event.listens_for(engine, "checkout")
def on_checkout(dbapi_conn, conn_record, conn_proxy):
    print(f"Connection checked out from pool")

# Pool status
pool = engine.pool
print(f"Pool size: {pool.size()}, checked out: {pool.checkedout()}")
```
