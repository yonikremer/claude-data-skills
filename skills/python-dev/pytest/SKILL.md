---
name: pytest
description: Use when writing or executing Python tests for unit, integration, or functional testing. Ideal for ensuring code quality and preventing regressions through clean syntax and powerful fixtures. CRITICAL: Always use descriptive test names and leverage fixtures for reusable setup logic.
---
# Pytest

## ⚠️ Mandatory Pre-flight: Resource Check

Large test suites, especially integration tests with databases or external APIs, can be slow and resource-intensive.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Parallel Execution**: If the system has multiple cores and the test suite is large (>50 tests), consider using `pytest-xdist` with `-n auto`.
3. **Database Isolation**: Ensure that tests requiring a database use a dedicated test instance to avoid data corruption.

## Common Pitfalls (The "Wall of Shame")

1. **State Leakage**: Tests that depend on the output of previous tests. Use fixtures with appropriate scopes to ensure isolation.
2. **Hardcoded Paths**: Tests that only run on the developer's machine. Use `tmp_path` fixture or `pathlib` for environment-agnostic paths.
3. **Slow Setup**: Repeating expensive setup in every test function. Use `module` or `session` scoped fixtures.

## References (Load on demand)
- `references/api-reference.md` — Formal signatures for pytest decorators and functions.

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
