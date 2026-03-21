---
name: s3
description: Read and write data to AWS S3 (and S3-compatible stores) using boto3, s3fs, and pandas. Use for storing and retrieving CSV/Parquet/JSON files, listing and managing objects, streaming large files, and building data pipelines with S3 as the data lake layer.
license: https://aws.amazon.com/
metadata:
    skill-author: K-Dense Inc.
---

# S3

## Installation

```bash
pip install boto3 s3fs
```

## Authentication

Credentials are resolved in this order automatically:
1. Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
2. `~/.aws/credentials` file
3. IAM role attached to EC2/ECS/Lambda (no config needed)

```python
import boto3

# Default credential chain (recommended)
s3 = boto3.client('s3')

# Explicit credentials
s3 = boto3.client('s3',
    aws_access_key_id='KEY',
    aws_secret_access_key='SECRET',
    region_name='us-east-1',
)

# S3-compatible endpoint (MinIO, Cloudflare R2, etc.)
s3 = boto3.client('s3',
    endpoint_url='https://my-minio.example.com',
    aws_access_key_id='KEY',
    aws_secret_access_key='SECRET',
)
```

## pandas — Read/Write Directly from S3

The simplest approach for data files — pandas uses `s3fs` under the hood:

```python
import pandas as pd

# CSV
df = pd.read_csv('s3://bucket/path/data.csv')
df.to_csv('s3://bucket/path/out.csv', index=False)

# Parquet
df = pd.read_parquet('s3://bucket/path/data.parquet')
df.to_parquet('s3://bucket/path/out.parquet', index=False)

# JSON lines
df = pd.read_json('s3://bucket/path/data.ndjson', lines=True)
df.to_json('s3://bucket/path/out.ndjson', orient='records', lines=True)

# With explicit credentials / custom endpoint
import s3fs
fs = s3fs.S3FileSystem(
    key='ACCESS_KEY',
    secret='SECRET_KEY',
    endpoint_url='https://...',   # omit for standard AWS
)
with fs.open('bucket/path/data.csv', 'rb') as f:
    df = pd.read_csv(f)

# Read multiple files (glob)
files = fs.glob('bucket/prefix/year=2024/**/*.parquet')
df = pd.concat(
    [pd.read_parquet(f's3://{f}') for f in files],
    ignore_index=True
)
```

## boto3 — Object Operations

```python
import boto3

s3 = boto3.client('s3')
BUCKET = 'my-bucket'

# Upload file
s3.upload_file('local_file.csv', BUCKET, 'path/in/s3/file.csv')

# Download file
s3.download_file(BUCKET, 'path/in/s3/file.csv', 'local_file.csv')

# Upload from in-memory bytes / string
import io
buf = io.BytesIO(b'hello world')
s3.upload_fileobj(buf, BUCKET, 'path/test.txt')

# Download to memory
buf = io.BytesIO()
s3.download_fileobj(BUCKET, 'path/test.txt', buf)
buf.seek(0)
content = buf.read()

# Read text object directly
resp = s3.get_object(Bucket=BUCKET, Key='path/file.txt')
text = resp['Body'].read().decode('utf-8')

# Delete
s3.delete_object(Bucket=BUCKET, Key='path/file.txt')

# Copy between buckets/paths
s3.copy_object(
    CopySource={'Bucket': 'source-bucket', 'Key': 'source/key'},
    Bucket='dest-bucket', Key='dest/key'
)
```

## Listing Objects

```python
# Simple listing (up to 1000 objects)
resp = s3.list_objects_v2(Bucket=BUCKET, Prefix='data/2024/')
for obj in resp.get('Contents', []):
    print(obj['Key'], obj['Size'], obj['LastModified'])

# Paginated listing (handles > 1000 objects)
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=BUCKET, Prefix='data/')

all_keys = []
for page in pages:
    for obj in page.get('Contents', []):
        all_keys.append(obj['Key'])

# List into a DataFrame
import pandas as pd

rows = []
for page in paginator.paginate(Bucket=BUCKET, Prefix='data/'):
    for obj in page.get('Contents', []):
        rows.append({
            'key':           obj['Key'],
            'size_bytes':    obj['Size'],
            'last_modified': obj['LastModified'],
        })
df_objects = pd.DataFrame(rows)

# List common prefixes (like ls on a directory)
resp = s3.list_objects_v2(Bucket=BUCKET, Prefix='data/', Delimiter='/')
for prefix in resp.get('CommonPrefixes', []):
    print(prefix['Prefix'])    # e.g. 'data/2024/'
```

## Streaming Large Files (no full download)

```python
import gzip, io, csv

# Stream and decompress a gzip CSV without downloading the whole file
resp = s3.get_object(Bucket=BUCKET, Key='data/large.csv.gz')
with gzip.open(resp['Body'], 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        process(row)

# Stream into pandas in chunks
resp = s3.get_object(Bucket=BUCKET, Key='data/large.csv')
chunks = pd.read_csv(resp['Body'], chunksize=100_000)
for chunk in chunks:
    process(chunk)

# Stream Parquet via pyarrow (columnar, efficient)
import pyarrow.parquet as pq
import s3fs

fs = s3fs.S3FileSystem()
pf = pq.ParquetFile(fs.open('bucket/path/data.parquet'))
for batch in pf.iter_batches(batch_size=50_000, columns=['id', 'val']):
    df = batch.to_pandas()
    process(df)
```

## Multipart Upload (large files)

boto3 handles multipart automatically via `upload_file` / `upload_fileobj`. For fine-grained control:

```python
from boto3.s3.transfer import TransferConfig

config = TransferConfig(
    multipart_threshold=100 * 1024 * 1024,   # 100 MB
    multipart_chunksize=50  * 1024 * 1024,   #  50 MB per part
    max_concurrency=10,
)
s3.upload_file('large_file.bin', BUCKET, 'path/large_file.bin',
               Config=config)
```

## Presigned URLs (temporary access)

```python
# Generate a URL that allows download without AWS credentials
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': BUCKET, 'Key': 'path/file.csv'},
    ExpiresIn=3600   # seconds
)
# url can be shared or used in requests.get(url)

# Presigned POST for browser uploads
post = s3.generate_presigned_post(
    BUCKET, 'uploads/file.csv',
    ExpiresIn=3600
)
# post['url'] and post['fields'] are used in the HTML form
```

## Common Patterns

```python
# Check if object exists (without try/except)
from botocore.exceptions import ClientError

def s3_key_exists(bucket: str, key: str) -> bool:
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        raise

# Partition writes by date (Hive-style partitioning)
import datetime

def write_partition(df: pd.DataFrame, bucket: str, prefix: str, date: datetime.date):
    key = f"{prefix}/year={date.year}/month={date.month:02d}/day={date.day:02d}/data.parquet"
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    buf.seek(0)
    s3.upload_fileobj(buf, bucket, key)

# Atomic write via temp key + rename (S3 has no rename; copy + delete)
def atomic_write_parquet(df: pd.DataFrame, bucket: str, final_key: str):
    tmp_key = final_key + '.tmp'
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    buf.seek(0)
    s3.upload_fileobj(buf, bucket, tmp_key)
    s3.copy_object(CopySource={'Bucket': bucket, 'Key': tmp_key},
                   Bucket=bucket, Key=final_key)
    s3.delete_object(Bucket=bucket, Key=tmp_key)
```
