# pandas I/O — Complete Reference

## CSV

```python
# Read
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv',
    sep='\t',                          # or ';', '|', etc.
    header=0,                          # row number for column names (None = no header)
    names=['a','b','c'],               # supply column names manually
    index_col='id',                    # use column as index
    usecols=['id','ts','val'],         # read only these columns
    dtype={'id': int, 'val': float},   # explicit types (avoids inference cost)
    parse_dates=['ts'],                # parse as datetime
    date_format='%Y-%m-%d %H:%M:%S',  # explicit format (faster)
    na_values=['NA','N/A','--'],       # extra null markers
    skiprows=3,                        # skip first N rows
    nrows=1000,                        # read at most N rows
    encoding='utf-8',                  # or 'latin1', 'cp1252'
    compression='gzip',               # 'gzip', 'bz2', 'zip', 'xz', 'zstd'
    chunksize=100_000,                 # returns iterator of chunks
    low_memory=False,                  # disable mixed-type warning
)

# Write
df.to_csv('out.csv', index=False)
df.to_csv('out.csv.gz', index=False, compression='gzip')
df.to_csv('out.tsv', sep='\t', index=False)
```

## JSON

```python
# Read
df = pd.read_json('data.json')                     # array of records
df = pd.read_json('data.json', lines=True)         # newline-delimited JSON (NDJSON / logs)
df = pd.read_json('data.json', orient='index')     # {row_id: {col: val}}
df = pd.read_json('data.json', orient='columns')   # {col: {row_id: val}}
df = pd.read_json(json_string)                     # from string

# Nested JSON — normalize first
import json
with open('nested.json') as f:
    raw = json.load(f)
df = pd.json_normalize(raw, record_path='records', meta=['id','name'])
df = pd.json_normalize(raw, sep='.')    # flatten nested keys with '.' separator

# Write
df.to_json('out.json', orient='records', indent=2)
df.to_json('out.ndjson', orient='records', lines=True)   # NDJSON (one record per line)
```

## Parquet (recommended for persistent storage)

```python
# Requires: pip install pyarrow   (or fastparquet)

# Read
df = pd.read_parquet('data.parquet')
df = pd.read_parquet('data.parquet', columns=['id','val'])   # column pruning
df = pd.read_parquet('data.parquet', filters=[('val', '>', 0)])  # row-group filtering

# Read partitioned dataset (directory)
df = pd.read_parquet('data_dir/')    # reads all .parquet files

# Write
df.to_parquet('out.parquet', index=False)
df.to_parquet('out.parquet', compression='snappy')   # or 'gzip', 'zstd', 'brotli'
df.to_parquet('out.parquet', engine='pyarrow')

# Write partitioned
df.to_parquet('out_dir/', partition_cols=['year','month'])
```

## SQL

```python
import pandas as pd
import sqlalchemy

# --- SQLite ---
engine = sqlalchemy.create_engine('sqlite:///mydb.sqlite')
# or in-memory: sqlalchemy.create_engine('sqlite://')

# --- PostgreSQL ---
engine = sqlalchemy.create_engine(
    'postgresql+psycopg2://user:pass@host:5432/dbname'
)

# --- Oracle ---
engine = sqlalchemy.create_engine(
    'oracle+cx_oracle://user:pass@host:1521/?service_name=SVC'
)

# --- Read ---
df = pd.read_sql('SELECT * FROM my_table WHERE val > 100', engine)
df = pd.read_sql_table('my_table', engine)
df = pd.read_sql_table('my_table', engine, schema='my_schema')
df = pd.read_sql_query(text("SELECT * FROM t WHERE id = :id"), engine,
                       params={'id': 42})

# Chunked read (large tables)
chunks = pd.read_sql('SELECT * FROM big_table', engine, chunksize=50_000)
df = pd.concat(chunks, ignore_index=True)

# --- Write ---
df.to_sql('my_table', engine, if_exists='replace', index=False)
df.to_sql('my_table', engine, if_exists='append',  index=False)
df.to_sql('my_table', engine, if_exists='fail',    index=False)

# Explicit dtypes mapping (important for Oracle / Postgres type precision)
from sqlalchemy import Integer, Float, String, DateTime
df.to_sql('my_table', engine, dtype={
    'id':        Integer(),
    'val':       Float(),
    'name':      String(100),
    'created_at': DateTime(),
}, index=False)
```

## S3

```python
# Requires: pip install s3fs boto3

# Credentials: set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars,
# or use ~/.aws/credentials, or IAM role (no config needed in that case)

# CSV
df = pd.read_csv('s3://bucket/path/data.csv')
df.to_csv('s3://bucket/path/out.csv', index=False)

# Parquet
df = pd.read_parquet('s3://bucket/path/data.parquet')
df.to_parquet('s3://bucket/path/out.parquet')

# With explicit credentials
import s3fs
fs = s3fs.S3FileSystem(
    key='ACCESS_KEY',
    secret='SECRET_KEY',
    client_kwargs={'endpoint_url': 'https://...'}  # for non-AWS S3 compatible
)
with fs.open('bucket/path/data.csv', 'rb') as f:
    df = pd.read_csv(f)

# Read multiple files
import s3fs
fs = s3fs.S3FileSystem()
files = fs.glob('bucket/prefix/*.parquet')
df = pd.concat([pd.read_parquet(f's3://{f}') for f in files], ignore_index=True)
```

## Excel

```python
# Read — requires openpyxl (xlsx) or xlrd (xls)
df = pd.read_excel('data.xlsx')
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df = pd.read_excel('data.xlsx', sheet_name=0)       # by position
df = pd.read_excel('data.xlsx', sheet_name=None)    # dict of all sheets

df = pd.read_excel('data.xlsx',
    header=1,                   # row 1 as header (0-indexed)
    usecols='A:E',              # column range
    usecols=[0, 2, 4],          # column positions
    skiprows=2,
    nrows=500,
    dtype={'id': int},
)

# Write
df.to_excel('out.xlsx', sheet_name='Results', index=False)

# Multiple sheets
with pd.ExcelWriter('out.xlsx', engine='openpyxl') as w:
    df1.to_excel(w, sheet_name='Data',    index=False)
    df2.to_excel(w, sheet_name='Summary', index=False)
```

## Chunked / Streaming Reads

For files too large to fit in RAM:

```python
# CSV chunks
total = 0
for chunk in pd.read_csv('big.csv', chunksize=100_000):
    total += chunk['val'].sum()

# Accumulate filtered rows
chunks = []
for chunk in pd.read_csv('big.csv', chunksize=100_000):
    chunks.append(chunk[chunk['status'] == 'active'])
df = pd.concat(chunks, ignore_index=True)

# SQL chunks
for chunk in pd.read_sql('SELECT * FROM big_table', engine, chunksize=50_000):
    process(chunk)
```

## Type Inference and Memory Optimization

```python
# After reading, optimize memory
def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes('object'):
        if df[col].nunique() / len(df) < 0.1:   # < 10% cardinality
            df[col] = df[col].astype('category')
    for col in df.select_dtypes('float64'):
        df[col] = pd.to_numeric(df[col], downcast='float')
    for col in df.select_dtypes('int64'):
        df[col] = pd.to_numeric(df[col], downcast='integer')
    return df

# Check savings
before = df.memory_usage(deep=True).sum()
df = optimize_dtypes(df)
after = df.memory_usage(deep=True).sum()
print(f'Memory reduced {before/1e6:.1f} MB → {after/1e6:.1f} MB')
```
