---
name: legacy-migration
description: Migrates legacy codebases (C#, MATLAB) to modern Python (3.9+). Use when translating business logic, mathematical models, or data pipelines into idiomatic Python.
---

# Legacy Migration (C# & MATLAB to Modern Python)

## Overview
This skill provides patterns and best practices for migrating legacy codebases from C# (.NET) and MATLAB to modern, idiomatic Python (3.9+).

## 1. C# (.NET) to Python Migration

### 1.1 Type Mapping
| C# Feature | Python Equivalent |
|------------|-------------------|
| `class`, `interface` | `class` (use `Protocol` for interfaces) |
| `List<T>`, `Dictionary<K,V>` | `list[T]`, `dict[K,V]` |
| `LINQ (Where, Select)` | List comprehensions, `filter()`, `map()` |
| `async`/`await` | `async`/`await` |
| `namespace` | Modules and Packages |
| `NuGet` | `pip` / `PyPI` |

### 1.2 LINQ to Idiomatic Python
**C# (LINQ):**
```csharp
var results = items.Where(x => x.Active).Select(x => x.Value).ToList();
```
**Python (Idiomatic):**
```python
results = [x.value for x in items if x.active]
```

### 1.3 Data Transfer Objects (DTOs)
Replace C# POCOs with Pydantic models or Dataclasses.
```python
from pydantic import BaseModel

class UserProfile(BaseModel):
    id: int
    username: str
    is_active: bool = True
```

## 2. MATLAB to Python (NumPy/SciPy) Migration

### 2.1 Fundamental Differences
- **Indexing**: MATLAB is 1-based; Python is 0-based.
- **Slicing**: MATLAB `a(1:3)` includes the 3rd element; Python `a[0:3]` does not.
- **Memory**: MATLAB is column-major; NumPy is row-major by default (C-style).

### 2.2 Syntax Mapping
| MATLAB | Python (NumPy) |
|--------|----------------|
| `[1, 2; 3, 4]` | `np.array([[1, 2], [3, 4]])` |
| `zeros(3,3)` | `np.zeros((3, 3))` |
| `a' (transpose)` | `a.T` or `a.conj().T` |
| `a .* b (element-wise)` | `a * b` |
| `a * b (matrix mult)` | `a @ b` |
| `inv(A)` | `np.linalg.inv(A)` |

### 2.3 Script Structure
Convert MATLAB functions in separate files into Python modules with a main entry point.
```python
import numpy as np

def calculate_model(data: np.ndarray) -> np.ndarray:
    # MATLAB: result = sum(data, 1)
    return np.sum(data, axis=0)

if __name__ == "__main__":
    test_data = np.random.rand(10, 5)
    print(calculate_model(test_data))
```

## 3. Modern Python Standards
- **Type Hints**: Always use `typing` for function signatures.
- **Project Structure**: Use `pyproject.toml` and a flat or `src` layout.
- **Virtual Envs**: Always use `venv` or `conda`.
- **Formatting**: Use `black` and `ruff`.

## 4. Common Pitfalls
- **Implicit Copies**: MATLAB often copies on assignment; Python references objects. Use `.copy()` in Python when necessary.
- **Exception Handling**: C# uses `try-catch-finally`; Python uses `try-except-finally-else`.
- **Global Scope**: MATLAB scripts often pollute the global workspace; encapsulate Python logic in functions/classes.
