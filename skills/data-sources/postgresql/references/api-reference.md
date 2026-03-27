# PostgreSQL API Reference

This document provides a reference for core functions and classes used for interacting with PostgreSQL.

## Psycopg2

### `psycopg2.connect(dsn=None, connection_factory=None, cursor_factory=None, **kwargs)`

Create a new database connection.

The connection parameters can be specified as a string:

    conn = psycopg2.connect("dbname=test user=postgres password=secret")

or using a set of keyword arguments:

    conn = psycopg2.connect(database="test", user="postgres", password="secret")

Or as a mix of both. The basic connection parameters are:

- *dbname*: the database name
- *database*: the database name (only as keyword argument)
- *user*: user name used to authenticate
- *password*: password used to authenticate
- *host*: database host address (defaults to UNIX socket if not provided)
- *port*: connection port number (defaults to 5432 if not provided)

Using the *connection_factory* parameter a different class or connections
factory can be specified. It should be a callable object taking a dsn
argument.

Using the *cursor_factory* parameter, a new default cursor factory will be
used by cursor().

Using *async*=True an asynchronous connection will be created. *async_* is
a valid alias (for Python versions where ``async`` is a keyword).

Any other keyword parameter will be passed to the underlying client
library: the list of supported parameters depends on the library version.

---

### `psycopg2.extras.execute_values(cur, sql, argslist, template=None, page_size=100, fetch=False)`

Execute a statement using `VALUES` with a sequence of parameters.

- **cur**: the cursor to use to execute the query.
- **sql**: the query to execute. It must contain a single `%s` placeholder, which will be replaced by a `VALUES list`.
    Example: `"INSERT INTO mytable (id, f1, f2) VALUES %s"`.
- **argslist**: sequence of sequences or dictionaries with the arguments to send to the query.
- **template**: the snippet to merge to every item in *argslist* to compose the query.
- **page_size**: maximum number of *argslist* items to include in every statement.
- **fetch**: if `True` return the query results into a list.

---

## SQLAlchemy & Pandas

For more advanced database interaction using an ORM or for direct integration with DataFrames:

- **[`sqlalchemy.create_engine`](../../sqlalchemy/references/api-reference.md)**: Create a new Engine instance.
- **[`pandas.read_sql`](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html)**: Read SQL query or database table into a DataFrame.
