---
name: dotenv
description: Manage configuration and secrets using environment variables and .env files. Use for database credentials, API keys, S3 config, and any value that varies between environments (dev/staging/prod). Covers python-dotenv, os.environ, and pydantic-settings for typed config objects.
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# dotenv and Config Management

## Quick Start

```bash
pip install python-dotenv
```

```ini
# .env file (never commit to git)
DATABASE_URL=postgresql://user:secret@localhost:5432/mydb
S3_BUCKET=my-data-bucket
AWS_REGION=us-east-1
BATCH_SIZE=1000
DEBUG=false
```

```python
from dotenv import load_dotenv
import os

load_dotenv()   # loads .env into os.environ (skips already-set vars)

db_url     = os.environ['DATABASE_URL']   # raises KeyError if missing
s3_bucket  = os.environ.get('S3_BUCKET', 'default-bucket')  # with default
batch_size = int(os.environ.get('BATCH_SIZE', '500'))
debug      = os.environ.get('DEBUG', 'false').lower() == 'true'
```

## python-dotenv Options

```python
from dotenv import load_dotenv, dotenv_values

# Load into environment
load_dotenv()                            # looks for .env in cwd and parents
load_dotenv('.env.production')           # specific file
load_dotenv(override=True)              # override already-set env vars
load_dotenv(verbose=True)               # print which file was loaded

# Load as dict (without touching os.environ)
config = dotenv_values('.env')
db_url = config['DATABASE_URL']

# Multiple files (later files override earlier)
config = {
    **dotenv_values('.env.base'),
    **dotenv_values('.env.local'),   # local overrides
    **os.environ,                    # actual environment always wins
}

# Find .env file (searches parent dirs too)
from dotenv import find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
```

## Typed Config with pydantic-settings

The cleanest approach — validates types, raises clear errors on missing vars:

```bash
pip install pydantic-settings
```

```python
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Required — raises if missing
    database_url: str
    aws_access_key_id: str
    aws_secret_access_key: str

    # Optional with defaults
    s3_bucket: str = 'my-default-bucket'
    aws_region: str = 'us-east-1'
    batch_size: int = 1000
    debug: bool = False
    log_level: str = Field(default='INFO', pattern='^(DEBUG|INFO|WARN|ERROR)$')

    # Optional (can be None)
    slack_webhook: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False    # DATABASE_URL or database_url both work

# Singleton pattern (load once, reuse everywhere)
settings = Settings()

# Use
from sqlalchemy import create_engine
engine = create_engine(settings.database_url)
```

## .env File Syntax

```ini
# Comments start with #
KEY=value                     # basic
KEY="value with spaces"       # quoted
KEY='another value'           # single quotes
KEY=                          # empty string

# Multiline (use quotes)
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAK...
-----END RSA PRIVATE KEY-----"

# Variable interpolation
BASE_DIR=/data
INPUT_DIR=${BASE_DIR}/input   # references BASE_DIR

# Export keyword (for shell compatibility)
export KEY=value
```

## .gitignore Setup

```gitignore
# Always ignore
.env
.env.local
.env.*.local

# Commit these (no secrets, just structure)
.env.example
.env.test
```

Maintain a `.env.example` with all keys but no real values:

```ini
# .env.example — commit this, not .env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET=
```

## os.environ Patterns

```python
import os

# Read
os.environ['KEY']                         # raises KeyError if missing
os.environ.get('KEY')                     # None if missing
os.environ.get('KEY', 'default')          # with default

# Check
'KEY' in os.environ

# Set (current process only, not persisted)
os.environ['KEY'] = 'value'

# Delete
del os.environ['KEY']
os.environ.pop('KEY', None)               # safe delete

# All env vars as dict
env_dict = dict(os.environ)

# Expand variables in strings
os.path.expandvars('$HOME/data')          # expands $HOME or %HOMEPATH%
```

## Environment-Specific Config

```python
import os
from dotenv import load_dotenv

ENV = os.environ.get('APP_ENV', 'development')

# Load base config, then override with env-specific
load_dotenv('.env')
load_dotenv(f'.env.{ENV}', override=True)

# .env           ← shared defaults
# .env.development  ← dev overrides
# .env.production   ← prod overrides (or real env vars in CI/CD)
```

## Passing Config to Subprocesses

```python
import subprocess, os

# Child process inherits parent's environment by default
subprocess.run(['python', 'worker.py'])

# Pass specific vars to a child process
env = os.environ.copy()
env['WORKER_ID'] = '42'
subprocess.run(['python', 'worker.py'], env=env)
```
