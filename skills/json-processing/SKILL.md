---
name: json-processing
description: Parses, queries, and transforms complex or nested JSON data. Use when handling API responses or flattening NDJSON logs into DataFrames. Do NOT use for format identification (use data-format-detection) or for general text parsing (use regex).
---
# JSON Processing

## Quick Start

```python
import json

# Parse
data = json.loads('{"id": 1, "name": "Alice"}')
data = json.load(open('data.json'))

# Serialize
s = json.dumps(data, indent=2)
json.dump(data, open('out.json', 'w'), indent=2)

# Common options
json.dumps(data, default=str)               # handle datetime/UUID etc → str
json.dumps(data, ensure_ascii=False)        # preserve unicode
json.dumps(data, separators=(',', ':'))     # compact (no spaces)
json.dumps(data, sort_keys=True)
```

## Fast Serialization with orjson

`orjson` is 3-10× faster than stdlib and natively handles datetime, UUID, numpy, pandas:

```python
# pip install orjson
import orjson

data = json.loads(orjson.dumps(obj))                    # serialize
obj  = orjson.loads(b'{"key": "value"}')                # deserialize (accepts bytes or str)

# orjson handles these natively — no custom encoder needed:
import datetime, uuid, numpy as np
orjson.dumps({
    'dt':    datetime.datetime.now(),
    'uid':   uuid.uuid4(),
    'arr':   np.array([1.0, 2.0, 3.0]),
})

# Options
orjson.dumps(data, option=orjson.OPT_INDENT_2)
orjson.dumps(data, option=orjson.OPT_SORT_KEYS)
orjson.dumps(data, option=orjson.OPT_NON_STR_KEYS)   # allow int dict keys
orjson.dumps(data, option=orjson.OPT_OMIT_MICROSECONDS)
```

## Nested JSON — Flattening and Normalization

### pandas json_normalize

```python
import pandas as pd

# Flat list of records
data = [{"id": 1, "name": "Alice", "address": {"city": "NY", "zip": "10001"}}]
df = pd.json_normalize(data)
# Columns: id, name, address.city, address.zip

# Nested arrays (record_path)
data = {"orders": [
    {"id": 1, "items": [{"sku": "A"}, {"sku": "B"}]},
    {"id": 2, "items": [{"sku": "C"}]},
]}
df = pd.json_normalize(data['orders'],
    record_path='items',           # expand this nested array
    meta=['id'],                   # include these fields from parent
    meta_prefix='order_',
)
# Columns: sku, order_id

# Custom separator
df = pd.json_normalize(data, sep='__')   # address__city instead of address.city

# Max depth
df = pd.json_normalize(data, max_level=1)
```

### Manual flattening for complex structures

```python
def flatten(obj, prefix='', sep='.') -> dict:
    """Recursively flatten a nested dict."""
    out = {}
    for k, v in obj.items():
        key = f'{prefix}{sep}{k}' if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key, sep))
        elif isinstance(v, list):
            out[key] = v   # keep lists as-is (or explode separately)
        else:
            out[key] = v
    return out

records = [flatten(r) for r in raw_records]
df = pd.DataFrame(records)
```

## JSONPath Queries

JSONPath lets you query nested JSON like XPath for XML:

```python
# pip install jsonpath-ng
from jsonpath_ng import parse

data = {
    "store": {
        "books": [
            {"title": "Moby Dick", "price": 8.99, "category": "fiction"},
            {"title": "Learning Python", "price": 29.99, "category": "tech"},
        ]
    }
}

# Find all titles
expr = parse('$.store.books[*].title')
titles = [m.value for m in expr.find(data)]
# ['Moby Dick', 'Learning Python']

# Filter: books with price < 10
expr = parse('$.store.books[?(@.price < 10)].title')
cheap = [m.value for m in expr.find(data)]

# Nested arrays in a list of records
expr = parse('$[*].address.city')
cities = [m.value for m in expr.find(records)]

# Update values in-place
expr = parse('$.store.books[*].price')
for match in expr.find(data):
    match.full_path.update(data, match.value * 1.1)   # apply 10% markup
```

## JSON Schema Validation

```python
# pip install jsonschema
import jsonschema

schema = {
    "type": "object",
    "required": ["id", "timestamp", "value"],
    "properties": {
        "id":        {"type": "integer"},
        "timestamp": {"type": "string", "format": "date-time"},
        "value":     {"type": "number", "minimum": 0},
        "tags":      {"type": "array", "items": {"type": "string"}},
        "metadata":  {"type": "object"},
    },
    "additionalProperties": False
}

# Validate one record
try:
    jsonschema.validate(instance=record, schema=schema)
except jsonschema.ValidationError as e:
    print(e.message)
    print(e.path)       # path to the failing field

# Validate many records, collecting errors
validator = jsonschema.Draft7Validator(schema)
for i, record in enumerate(records):
    errors = list(validator.iter_errors(record))
    if errors:
        print(f"Record {i}: {[e.message for e in errors]}")
```

## NDJSON (Newline-Delimited JSON) — Log Files and Streams

```python
import json
import pandas as pd

# Read NDJSON file
def read_ndjson(path: str) -> pd.DataFrame:
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Skipping bad line: {e}")
    return pd.DataFrame(records)

# Write NDJSON
def write_ndjson(df: pd.DataFrame, path: str):
    with open(path, 'w') as f:
        for record in df.to_dict('records'):
            f.write(json.dumps(record, default=str) + '\n')

# pandas shorthand (uses internal NDJSON reader)
df = pd.read_json('data.ndjson', lines=True)
df.to_json('out.ndjson', orient='records', lines=True)
```

## JSON in DataFrames (JSON Column)

When a DataFrame column contains JSON strings:

```python
import pandas as pd, json

df = pd.DataFrame({'id': [1, 2], 'payload': ['{"a": 1, "b": 2}', '{"a": 3, "b": 4}']})

# Parse a JSON string column
parsed = df['payload'].apply(json.loads)

# Extract a specific field
df['a'] = df['payload'].apply(lambda s: json.loads(s).get('a'))

# Expand all fields as columns
expanded = pd.json_normalize(df['payload'].apply(json.loads).tolist())
df = pd.concat([df.drop(columns=['payload']), expanded], axis=1)
```

## Custom Encoder / Decoder

```python
import json, datetime, uuid

class AppEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)

json.dumps(data, cls=AppEncoder)

# Custom decoder (convert ISO timestamps back to datetime on load)
def date_decoder(d: dict) -> dict:
    for k, v in d.items():
        if isinstance(v, str):
            try:
                d[k] = datetime.datetime.fromisoformat(v)
            except ValueError:
                pass
    return d

data = json.loads(s, object_hook=date_decoder)
```

## Performance Tips

```python
# orjson is fastest for both loads and dumps
import orjson
obj = orjson.loads(raw_bytes)
raw = orjson.dumps(obj)

# For large files, stream line by line instead of json.load() the whole file
with open('big.json') as f:
    data = json.load(f)   # loads everything into RAM

# Better: if it's actually NDJSON
with open('big.ndjson') as f:
    for line in f:
        process(json.loads(line))

# ijson — streaming parser for large single JSON objects
# pip install ijson
import ijson
with open('large.json', 'rb') as f:
    for record in ijson.items(f, 'records.item'):  # 'records' is the array key
        process(record)
```
