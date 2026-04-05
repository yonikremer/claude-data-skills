# SQLAlchemy API Reference

## `sqlalchemy.create_engine(url, **kwargs)`

Create a new Engine instance.

- **url**: Database URL (e.g., `postgresql+psycopg2://user:pass@host/db`)
- **pool_size**: The number of connections to keep open inside the connection pool.
- **pool_pre_ping**: If True, tests connections for liveness upon each checkout.

## `sqlalchemy.text(text)`

Construct a new TextClause, representing a textual SQL string directly.

- **text**: The SQL statement. Use `:name` for bind parameters.

## `sqlalchemy.select(*entities)`

Construct a new Select statement.

- **entities**: Columns or Tables to select from.

## `sqlalchemy.insert(table)`

Construct an Insert statement.

## `sqlalchemy.update(table)`

Construct an Update statement.

## `sqlalchemy.delete(table)`

Construct a Delete statement.

## `sqlalchemy.Table(name, metadata, *args, **kw)`

Represent a table in a database.

## `sqlalchemy.MetaData()`

A collection of Table objects and their associated schema constructs.

## `sqlalchemy.Column(name, type, *args, **kwargs)`

Represents a column in a database table.

## `sqlalchemy.orm.Session(bind, ...)`

Manages persistence operations for ORM-mapped objects.
