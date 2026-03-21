---
name: python-best-practices
description: Enforces PEP-8, idiomatic Python (Pythonic), and formatting standards. Use to ensure code quality, readability, and to avoid common pitfalls. Tests and coverage are recommended for production but optional for fast research scripts.
---
# Python Best Practices & Standards

This skill defines the coding standards for this project. Adhering to these ensures that code is readable, maintainable, and performs well, whether it's a one-off research script or a production-ready tool.

## 1. Code Style & Formatting

We prioritize automated formatting to reduce cognitive load and "nitpicking" during reviews.

### Tooling (Mandatory for non-trivial scripts)
- **`ruff`**: Use as the primary linter and formatter. It is 10-100x faster than alternatives and combines the power of Flake8, isort, and more.
- **`black`**: If `ruff` is not used, `black` is the fallback for deterministic formatting.

```bash
# Quick format and fix
ruff format .
ruff check --fix .
```

### Auto-Formatting (MANDATORY ACTION)
Before delivering or committing any Python code, you MUST run auto-formatting tools. This ensures the code is clean, consistent, and follows project standards without manual effort.

- **Action**: Execute `ruff format .` and `ruff check --fix .` in the project root or on specific files.
- **Benefit**: Fixes common PEP-8 issues, sorts imports, and removes unused variables automatically.

### PEP-8 Essentials
- **Naming**: 
  - `snake_case` for functions, variables, and modules.
  - `PascalCase` for classes.
  - `UPPER_SNAKE_CASE` for constants.
- **Line Length**: Prefer 88 (Black default) or 100 characters.
- **Indentation**: Always 4 spaces. Never tabs.

## 2. Idiomatic Python (Pythonic)

Avoid "Java-isms" or "C-isms". Use the language's strengths.

### Common Patterns
- **Comprehensions**: Use list/dict/set comprehensions for simple transformations. Use generator expressions for large datasets to save memory.
- **Truthiness**: Use `if items:` instead of `if len(items) > 0:`.
- **Enumerate**: Use `for i, item in enumerate(items):` instead of `range(len(items))`.
- **Context Managers**: Always use `with open(...) as f:` for file I/O to ensure proper closing.
- **Unpacking**: Use `a, b = b, a` for swapping and `first, *rest = items` for slicing.

## 3. Common Pitfalls & Anti-Patterns

### ❌ Mutable Default Arguments
Never use `[]` or `{}` as default arguments.
```python
# BAD
def add_item(item, items=[]): ...

# GOOD
def add_item(item, items=None):
    if items is None:
        items = []
```

### ❌ Bare Except
Never use `except:`. Always catch specific exceptions.
```python
# BAD
try: ... except: pass

# GOOD
try: ... except ValueError: ...
```

### ❌ Shadowing Built-ins
Avoid using names like `id`, `list`, `dict`, `str`, `input` for your variables.

### ❌ `type()` vs `isinstance()`
Use `isinstance(obj, Class)` because it respects inheritance. `type(obj) == Class` does not.

## 4. Data Safety & Integrity (CRITICAL)

To prevent irreversible data loss, especially during autonomous execution:

- **No Overwriting**: Never use `inplace=True` or overwrite original files (e.g., `data.csv`) without explicit permission.
- **Suffix Strategy**: Always create new files with suffixes for processed data (e.g., `data_cleaned.csv`, `results_v1.parquet`).
- **New Columns**: Prefer adding new columns (e.g., `df['value_normalized']`) instead of transforming columns in-place.
- **Confirmation**: If a task *requires* deletion (e.g., "Clean up temporary files"), ask for explicit confirmation before executing `os.remove()` or `shutil.rmtree()`.

## 5. Testing Strategy (Tiered Approach)

We recognize that not all code requires 100% coverage.

### Tier 1: Fast Research Scripts
- **Standard**: No mandatory tests.
- **Focus**: Correctness of output. 
- **Requirement**: Use `assert` statements within the script to verify data integrity at critical steps.

### Tier 2: Utility Tools / Shared Scripts
- **Standard**: Basic unit tests for core logic using `pytest`.
- **Requirement**: Test the "happy path" and common edge cases.

### Tier 3: Production / Core Library
- **Standard**: Comprehensive test suite, high coverage, and integration tests.
- **Requirement**: Mandatory `pytest` with documentation and type hints (`mypy`/`pyright` compatible).

## 5. Performance for Data Science

- **Vectorization**: If using `pandas` or `numpy`, avoid loops (`for`, `iterrows`). Use vectorized operations.
- **Lazy Loading**: Use `yield` generators or Polars lazy mode for data that doesn't fit in memory.
- **Pre-allocation**: If you must use a loop and know the size, pre-allocate the list/array instead of repeatedly appending.

## 6. Reproducibility & Randomness (MANDATORY)

To ensure research results are replicable, every script involving randomness MUST use a fixed seed.

- **Global Constant**: Standardize on `RANDOM_STATE = 42`.
- **Implementation**: 
  - NumPy: `np.random.seed(RANDOM_STATE)`
  - Scikit-Learn: `train_test_split(..., random_state=RANDOM_STATE)`
  - PyTorch: `torch.manual_seed(RANDOM_STATE)`
- **Rule**: Never leave `random_state` or `seed` as `None` in an invocable script.

## 7. Documentation

- **Docstrings**: Use Google or NumPy style for public-facing functions.
- **Type Hints**: Highly encouraged for all function signatures to enable better IDE support and catch bugs early.
- **Comments**: Explain *why* something is done, not *what* is being done (the code should show the *what*).
