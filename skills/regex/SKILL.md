---
name: regex
description: Parses and transforms text using regular expressions. Use when extracting fields from logs or validating complex string formats. Do NOT use for simple string methods or for parsing structured data (use json-processing).
---
# Regular Expressions (Python)

## Quick Reference

```python
import re

# Core functions
re.match(pattern, s)      # match at start of string only
re.search(pattern, s)     # first match anywhere
re.findall(pattern, s)    # list of all matches (strings)
re.finditer(pattern, s)   # iterator of Match objects
re.sub(pattern, repl, s)  # replace all matches
re.split(pattern, s)      # split string by pattern
re.fullmatch(pattern, s)  # match must cover entire string

# Always compile patterns used more than once
pat = re.compile(r'\d+')
pat.findall('abc 123 def 456')   # ['123', '456']
```

## Syntax Reference

### Character Classes

| Pattern | Matches |
|---------|---------|
| `.` | any char except newline (use `re.DOTALL` for all) |
| `\d` | digit `[0-9]` |
| `\D` | non-digit |
| `\w` | word char `[a-zA-Z0-9_]` |
| `\W` | non-word |
| `\s` | whitespace `[ \t\n\r\f\v]` |
| `\S` | non-whitespace |
| `[abc]` | any of a, b, c |
| `[^abc]` | anything except a, b, c |
| `[a-z]` | range |
| `[a-zA-Z0-9]` | alphanumeric |

### Quantifiers

| Pattern | Meaning |
|---------|---------|
| `*` | 0 or more (greedy) |
| `+` | 1 or more (greedy) |
| `?` | 0 or 1 |
| `{n}` | exactly n |
| `{n,m}` | n to m |
| `*?` `+?` `??` | lazy (non-greedy) versions |

### Anchors and Boundaries

| Pattern | Meaning |
|---------|---------|
| `^` | start of string (or line with `re.MULTILINE`) |
| `$` | end of string (or line with `re.MULTILINE`) |
| `\b` | word boundary |
| `\B` | non-word boundary |
| `\A` | start of string (ignores `MULTILINE`) |
| `\Z` | end of string (ignores `MULTILINE`) |

### Groups

```python
# Capturing group — captured in .group(1), findall returns group content
r'(\d{4})-(\d{2})-(\d{2})'

# Named group — captured as .group('year') or match.groupdict()
r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'

# Non-capturing group — group for alternation/repetition, not captured
r'(?:foo|bar)+'

# Backreference — match same text as group 1 again
r'(\w+) \1'   # matches "hello hello"

# Named backreference
r'(?P<word>\w+) (?P=word)'
```

### Lookahead and Lookbehind

```python
# Positive lookahead: match X only if followed by Y
r'\d+(?= dollars)'         # '100' in '100 dollars'

# Negative lookahead: match X only if NOT followed by Y
r'\d+(?! dollars)'         # '100' in '100 euros'

# Positive lookbehind: match X only if preceded by Y
r'(?<=\$)\d+'              # '100' in '$100'

# Negative lookbehind: match X only if NOT preceded by Y
r'(?<!\$)\d+'              # '100' in '100' but not '$100'
```

## Common Patterns

```python
# Email (simplified)
EMAIL = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

# IPv4 address
IPV4 = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# UUID
UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)

# ISO 8601 datetime
DATETIME = re.compile(
    r'\d{4}-\d{2}-\d{2}'              # date
    r'[T ]\d{2}:\d{2}:\d{2}'          # time
    r'(?:\.\d+)?'                      # optional fractional seconds
    r'(?:Z|[+-]\d{2}:?\d{2})?'        # optional timezone
)

# HTTP method + path
HTTP_REQUEST = re.compile(r'"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS) ([^ ]+) HTTP/[\d.]+"')

# Key=value pairs
KV = re.compile(r'(\w+)=(?:"([^"]*)"|([\S]*))')

# Semantic version
SEMVER = re.compile(r'(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+([a-zA-Z0-9.]+))?')

# Number (int or float, with optional sign)
NUMBER = re.compile(r'[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')
```

## Extracting Data

```python
import re

# Extract one value
m = re.search(r'duration=(\d+)ms', 'request duration=142ms latency')
if m:
    ms = int(m.group(1))   # 142

# Extract named groups
m = re.search(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})',
    '2024-03-15'
)
if m:
    d = m.groupdict()   # {'year': '2024', 'month': '03', 'day': '15'}

# Extract all matches
ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', log_line)

# Extract all matches with groups (findall returns list of tuples)
pairs = re.findall(r'(\w+)=(\w+)', 'a=1 b=2 c=3')
# [('a', '1'), ('b', '2'), ('c', '3')]

# Use finditer for large texts (lazy, no list allocation)
for m in re.finditer(r'ERROR.*', log_text):
    process(m.group(), m.start(), m.end())
```

## Replace and Transform

```python
# Simple replace
re.sub(r'\s+', ' ', text)              # collapse whitespace
re.sub(r'^\s+|\s+$', '', text)         # strip (like .strip())

# Replace with backreference
re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', '2024-03-15')  # → '15/03/2024'

# Replace with function
def mask_ip(m):
    parts = m.group().split('.')
    return '.'.join(parts[:2] + ['x', 'x'])

re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', mask_ip, log_line)

# Count replacements
result, n = re.subn(r'\d+', 'NUM', 'a1 b2 c3')   # n=3

# Split on multiple delimiters
re.split(r'[,;|\t]+', line)
re.split(r'\s*,\s*', 'a, b,  c')    # ['a', 'b', 'c']
```

## Flags

```python
re.compile(r'hello', re.IGNORECASE)   # case-insensitive (re.I)
re.compile(r'^line', re.MULTILINE)    # ^ matches start of each line (re.M)
re.compile(r'.+',    re.DOTALL)       # . matches newline (re.S)
re.compile(r'\d +',  re.VERBOSE)      # allow spaces/comments in pattern (re.X)

# Verbose pattern — use for complex regexes
PATTERN = re.compile(r"""
    (?P<year>  \d{4}) -   # year
    (?P<month> \d{2}) -   # month
    (?P<day>   \d{2})     # day
""", re.VERBOSE)

# Inline flags within pattern (useful when you can't pass flags)
r'(?i)hello'    # case-insensitive
r'(?m)^line'    # multiline
r'(?s).+'       # dotall
r'(?x) \d + \. \d +'   # verbose
```

## pandas Integration

```python
import pandas as pd

# str.extract — first match, groups → columns
df['year'] = df['date_str'].str.extract(r'(\d{4})')
df[['year', 'month', 'day']] = df['date_str'].str.extract(r'(\d{4})-(\d{2})-(\d{2})')

# Named groups
df = df.join(df['date_str'].str.extract(r'(?P<year>\d{4})-(?P<month>\d{2})'))

# str.extractall — all matches (MultiIndex result)
df_all = df['message'].str.extractall(r'(\d+)')   # all numbers per row

# str.findall — list of all matches per row
df['all_ips'] = df['message'].str.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# str.contains / str.match
df[df['message'].str.contains(r'ERROR|FATAL', regex=True, na=False)]
df[df['url'].str.match(r'^https://')]

# str.replace
df['clean'] = df['text'].str.replace(r'\s+', ' ', regex=True)
df['masked'] = df['text'].str.replace(r'\d{4}-\d{4}-\d{4}-\d{4}', 'XXXX-XXXX-XXXX-XXXX', regex=True)

# str.split with expand
df[['host', 'port']] = df['address'].str.split(':', expand=True, n=1)
```

## Performance

```python
# Always compile patterns used in loops
pat = re.compile(r'\d+')   # compile once
for line in lines:
    pat.findall(line)       # reuse compiled pattern

# Avoid catastrophic backtracking — use atomic groups or possessive quantifiers
# if needed (requires the 'regex' library for possessive quantifiers)

# Use str methods when regex isn't needed
s.startswith('foo')         # faster than re.match(r'^foo', s)
'foo' in s                  # faster than re.search(r'foo', s)
s.replace('a', 'b')         # faster than re.sub(r'a', 'b', s)

# regex library — superset of re with better performance and more features
# pip install regex
import regex
regex.findall(r'\p{L}+', text)   # Unicode letter category
regex.fullmatch(r'(\w+)+', text, timeout=1.0)  # timeout for safety
```
