---
name: python-core-pro
description: Use for writing ANY high-quality Python code. Consolidated expert guide for Best Practices (PEP-8), Type Safety (Pydantic), Testing (Pytest), CLI Scripts, and Performance (Parallelism). CRITICAL: Apply to all Python code generation and refactoring.
---
# Python Core Pro (Consolidated)

Unified expert guide for writing idiomatic, robust, and high-performance Python code.

## ⚠️ Mandatory Pre-flight: Standards & Quality

1. **PEP-8 First**: Always adhere to standard Python formatting (or use `black`/`ruff`).
2. **Type Hints**: Use type annotations for all function signatures to improve readability and catch bugs.
3. **Fail Loudly**: Never catch `Exception` or `ImportError` silently.

---

## 1. Modern Best Practices & Idioms

Use for writing clean, maintainable Python code.

### Core Idioms
- **Pathlib**: Always use `pathlib.Path` instead of `os.path`.
- **Context Managers**: Use `with` for file I/O, database sessions, and network connections.
- **F-Strings**: Use literal string interpolation for all formatting.

```python
from pathlib import Path

def process_file(path_str: str) -> None:
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    
    with path.open('r') as f:
        data = f.read()
```

---

## 2. Type Safety & Validation (Pydantic)

Use for validating data structures and managing configuration.

### Core Idiom
- **Strict Typing**: Use Pydantic V2 models for all data-heavy structures.

```python
from pydantic import BaseModel, Field

class Config(BaseModel):
    db_url: str = Field(..., description="Database connection string")
    max_retries: int = 3
```

---

## 3. Testing (Pytest)

Use for writing and executing robust tests.

### Core Idioms
- **Fixtures**: Use `pytest.fixture` for reusable setup/teardown.
- **Parametrization**: Use `pytest.mark.parametrize` for testing multiple scenarios.

---

## 4. Performance & Parallelism

Use for accelerating I/O-bound (Multithreading) and CPU-bound (Multiprocessing) tasks.

### Core Tools
- **ThreadPoolExecutor**: For network requests and file I/O.
- **ProcessPoolExecutor**: For heavy numerical computations.

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **Mutable Defaults**: Using `def func(x=[])`. Use `def func(x=None)` and initialize inside.
2. **Bare Excepts**: `except: pass` (The "Black Hole" anti-pattern).
3. **Global State**: Overusing global variables instead of passing arguments or using classes.

## References
- `skills/python-dev/python-core-pro/references/stdlib/` — Detailed PEP-8 and idiom guide.
- `skills/python-dev/python-core-pro/references/pydantic/` — Advanced V2 patterns and validation.
- `skills/python-dev/python-core-pro/references/pytest/` — Mocking and complex fixture patterns.
