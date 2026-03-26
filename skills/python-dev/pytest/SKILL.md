---
name: pytest
description: Writes and executes Python tests with clean syntax and powerful fixtures. Use for unit testing, integration testing, and ensuring code quality. Do NOT use for basic scripts that don't require verification.
---
# Pytest

Pytest is the standard testing framework for Python, offering a simple syntax, powerful fixtures, and detailed failure reports.

## Getting Started

```bash
uv pip install pytest
```

### Simple Test

Save in `test_logic.py`:
```python
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
```

Run with:
```bash
pytest
```

## Core Features

### 1. Assertions
Use standard Python `assert`. Pytest provides "assertion rewriting" for detailed error messages showing exactly what failed.

### 2. Fixtures
Reusable setup and teardown logic.

```python
import pytest
import pandas as pd

@pytest.fixture
def sample_df():
    return pd.DataFrame({'a': [1, 2], 'b': [3, 4]})

def test_dataframe_shape(sample_df):
    assert sample_df.shape == (2, 2)
```

**Scope**: Control how often fixtures run:
- `function` (default): every test
- `module`: once per file
- `session`: once per entire run

### 3. Parameterization
Run a test with multiple inputs.

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (5, 10),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### 4. Handling Exceptions

```python
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

## Best Practices

1.  **Naming**: Files should be `test_*.py`, functions should be `test_*`.
2.  **Structure**: Keep tests in a `tests/` directory.
3.  **Clean Up**: Use the `yield` keyword in fixtures for teardown.
    ```python
    @pytest.fixture
    def db_conn():
        conn = connect()
        yield conn
        conn.close()
    ```
4.  **Marking**: Categorize tests (e.g., `@pytest.mark.slow`).

## Useful CLI Options

- `pytest -v`: Verbose output.
- `pytest -k "name"`: Run tests matching "name".
- `pytest -x`: Stop after the first failure.
- `pytest --lf`: Run only the last failed tests.
- `pytest --cov=src`: Check test coverage (requires `pytest-cov`).

## Resources

- Official Docs: https://docs.pytest.org/
- Fixture Reference: https://docs.pytest.org/en/stable/explanation/fixtures.html
