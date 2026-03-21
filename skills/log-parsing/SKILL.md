---
name: log-parsing
description: Parses structured and unstructured log files into DataFrames for analysis. Use when processing syslog, access logs, or application logs. Do NOT use for real-time monitoring (use elasticsearch) or for simple text search (use regex).
---
# Log Parsing

## Overview

Log parsing in Python falls into three patterns:
- **Regex extraction** — unstructured text logs with known formats
- **JSON log parsing** — structured logs (one JSON object per line)
- **Python `logging` / `structlog`** — parsing your own application's log output

## JSON Logs (Structured)

Most modern applications emit newline-delimited JSON (NDJSON):

```python
import json
import pandas as pd

# Read NDJSON log file
records = []
with open('app.log') as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # skip malformed lines

df = pd.DataFrame(records)

# From S3
import s3fs
fs = s3fs.S3FileSystem()
records = []
with fs.open('bucket/logs/app.log.gz', 'rt', compression='gzip') as f:
    for line in f:
        try:
            records.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            pass
df = pd.DataFrame(records)
```

## Regex-Based Parsing

### Apache / nginx Combined Log Format

```
127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326
```

```python
import re
import pandas as pd
from datetime import datetime

COMBINED_LOG = re.compile(
    r'(?P<ip>\S+)'           # client IP
    r' \S+'                  # ident (usually -)
    r' (?P<user>\S+)'        # auth user
    r' \[(?P<time>[^\]]+)\]' # timestamp
    r' "(?P<method>\S+)'     # HTTP method
    r' (?P<path>\S+)'        # request path
    r' \S+"'                 # protocol
    r' (?P<status>\d{3})'    # status code
    r' (?P<bytes>\S+)'       # bytes sent
    r'(?: "(?P<referer>[^"]*)")?'   # referer (optional)
    r'(?: "(?P<agent>[^"]*)")?'     # user agent (optional)
)

def parse_apache_log(path: str) -> pd.DataFrame:
    records = []
    with open(path) as f:
        for line in f:
            m = COMBINED_LOG.match(line)
            if m:
                d = m.groupdict()
                d['time'] = datetime.strptime(d['time'], '%d/%b/%Y:%H:%M:%S %z')
                d['status'] = int(d['status'])
                d['bytes'] = int(d['bytes']) if d['bytes'] != '-' else 0
                records.append(d)
    return pd.DataFrame(records)
```

### Syslog Format

```
Jan 15 10:23:45 myhost myapp[1234]: Connection refused to 10.0.0.1:5432
```

```python
SYSLOG = re.compile(
    r'(?P<month>\w{3})\s+(?P<day>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2})'
    r' (?P<host>\S+)'
    r' (?P<program>[^\[:\s]+)(?:\[(?P<pid>\d+)\])?'
    r': (?P<message>.+)'
)

def parse_syslog(path: str) -> pd.DataFrame:
    records = []
    with open(path) as f:
        for line in f:
            m = SYSLOG.match(line.strip())
            if m:
                records.append(m.groupdict())
    df = pd.DataFrame(records)
    # Reconstruct full timestamp (syslog has no year)
    import datetime
    current_year = datetime.datetime.now().year
    df['timestamp'] = pd.to_datetime(
        df['month'] + ' ' + df['day'] + ' ' + str(current_year) + ' ' + df['time'],
        format='%b %d %Y %H:%M:%S'
    )
    return df
```

### Generic Key=Value Logs

```
2024-01-15 10:23:45 level=ERROR service=auth user_id=42 latency_ms=1523 msg="Login failed"
```

```python
import re

KV_PATTERN = re.compile(r'(\w+)=(".*?"|\S+)')
TIMESTAMP   = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

def parse_kv_log(line: str) -> dict:
    d = {}
    ts_match = TIMESTAMP.match(line)
    if ts_match:
        d['timestamp'] = ts_match.group()
    for key, val in KV_PATTERN.findall(line):
        d[key] = val.strip('"')
    return d

records = []
with open('app.log') as f:
    for line in f:
        records.append(parse_kv_log(line.strip()))
df = pd.DataFrame(records)
```

## Chunked / Large File Parsing

```python
import gzip
from pathlib import Path

def iter_log_lines(path: str, encoding='utf-8', errors='replace'):
    """Transparently handle .gz and plain files."""
    p = Path(path)
    opener = gzip.open if p.suffix == '.gz' else open
    with opener(path, 'rt', encoding=encoding, errors=errors) as f:
        yield from f

# Parse in chunks to avoid loading everything into memory
CHUNK = 100_000
records = []
for i, line in enumerate(iter_log_lines('large.log.gz')):
    m = COMBINED_LOG.match(line)
    if m:
        records.append(m.groupdict())
    if len(records) >= CHUNK:
        process(pd.DataFrame(records))
        records = []
if records:
    process(pd.DataFrame(records))
```

## Common Analysis Patterns

```python
df = parse_apache_log('access.log')
df['time'] = pd.to_datetime(df['time'])
df = df.set_index('time').sort_index()

# Error rate over time
df.resample('5min')['status'].apply(lambda s: (s >= 400).mean()).plot()

# Top paths by 5xx errors
df[df['status'] >= 500]['path'].value_counts().head(20)

# Slow requests (if latency is in the log)
df[df['latency_ms'] > 1000].sort_values('latency_ms', ascending=False)

# Unique IPs per hour
df.resample('h')['ip'].nunique()

# Parse timestamp from log field
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
df['hour'] = df['timestamp'].dt.hour
df['weekday'] = df['timestamp'].dt.day_name()
```

## Python `logging` — Parse Your Own App Logs

```python
import logging
import re

# Standard Python logging format:
# 2024-01-15 10:23:45,123 ERROR mymodule:42 - Something went wrong
LOG_RECORD = re.compile(
    r'(?P<asctime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})'
    r' (?P<levelname>\w+)'
    r' (?P<name>[^:]+):(?P<lineno>\d+)'
    r' - (?P<message>.+)'
)

# Or emit JSON logs from your application (easier to parse):
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'ts':      self.formatTime(record, '%Y-%m-%dT%H:%M:%S'),
            'level':   record.levelname,
            'name':    record.name,
            'line':    record.lineno,
            'message': record.getMessage(),
        })

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(handler)
```

## Extract Specific Patterns from Free-Text Messages

```python
import re

# Extract IPs
IP_RE = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# Extract UUIDs
UUID_RE = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)

# Extract durations like "1.23s", "456ms"
DURATION_RE = re.compile(r'(\d+(?:\.\d+)?)\s*(ms|s|µs|us)', re.I)

df['ips']       = df['message'].str.findall(IP_RE.pattern)
df['has_uuid']  = df['message'].str.contains(UUID_RE.pattern, regex=True)
df['duration']  = df['message'].str.extract(r'(\d+(?:\.\d+)?)\s*ms').astype(float)
```
