---
name: refactoring
description: Use when improving code quality and restructuring Python codebases using automated tools. Ideal for cleaning up legacy scripts or applying project-wide formatting. Do NOT use for initial feature implementation or for version control (use git).
---
# Refactoring and Large-Scale Fixing

## Automated Tools (run first)

Apply these in order before any manual refactoring:

```bash
# Install all tools
pip install ruff black isort pyupgrade

# 1. pyupgrade — modernize Python syntax (f-strings, type hints, etc.)
pyupgrade --py39-plus **/*.py

# 2. isort — sort and organize imports
isort .
isort --diff .   # preview only

# 3. black — format code consistently
black .
black --diff .   # preview only
black --check .  # CI mode (exit 1 if any file would change)

# 4. ruff — fast linter that catches real bugs and anti-patterns
ruff check .
ruff check --fix .         # auto-fix safe rules
ruff check --fix --unsafe-fixes .  # also apply unsafe fixes

# Combined: ruff can replace isort + many other tools
ruff format .              # ruff's formatter (black-compatible)
ruff check --select I --fix .   # isort-compatible import sorting
```

### ruff configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = [
    "E", "W",   # pycodestyle
    "F",        # pyflakes (unused imports, undefined names)
    "I",        # isort
    "UP",       # pyupgrade
    "B",        # flake8-bugbear (common bugs)
    "C4",       # flake8-comprehensions
    "SIM",      # flake8-simplify
    "RUF",      # ruff-specific
]
ignore = ["E501"]  # line too long (handled by formatter)

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]  # allow assert in tests
```

## Common Anti-Patterns and Fixes

### Mutable default arguments

```python
# BAD — the list is shared across all calls
def process(data, results=[]):
    results.append(data)
    return results

# GOOD
def process(data, results=None):
    if results is None:
        results = []
    results.append(data)
    return results
```

### Bare except

```python
# BAD — catches SystemExit, KeyboardInterrupt, etc.
try:
    do_something()
except:
    pass

# GOOD
try:
    do_something()
except Exception as e:
    log.error(f"Failed: {e}")
```

### Using `type()` instead of `isinstance()`

```python
# BAD — doesn't respect inheritance
if type(x) == list:
    ...

# GOOD
if isinstance(x, list):
    ...
```

### Unnecessary list() around comprehensions / generators

```python
# BAD
sum([x * 2 for x in items])   # list comprehension passed to sum
any([condition(x) for x in items])

# GOOD — generator expressions are lazy and more memory-efficient
sum(x * 2 for x in items)
any(condition(x) for x in items)
```

### String concatenation in loops

```python
# BAD — O(n²) due to string immutability
result = ""
for item in items:
    result += str(item) + ", "

# GOOD
result = ", ".join(str(item) for item in items)
```

### Repeated attribute lookup in hot loops

```python
# BAD
for i in range(1000000):
    result = math.sqrt(i)   # looks up math.sqrt each iteration

# GOOD
sqrt = math.sqrt
for i in range(1000000):
    result = sqrt(i)
```

### God functions / long functions

Break long functions by extracting logical sections:

```python
# Before: 200-line function doing everything
def process_data(df):
    # 50 lines: load and validate
    # 50 lines: clean
    # 50 lines: transform
    # 50 lines: output

# After: compose small functions
def process_data(df):
    df = validate_schema(df)
    df = clean_data(df)
    df = transform(df)
    return write_output(df)
```

## Systematic Large-Scale Fixes

### Find and fix across a codebase

```bash
# Find all occurrences of a pattern
grep -rn "\.iteritems()" src/
grep -rn "print " src/ | grep -v "print("   # old print statements

# Sed for simple replacements (backup first)
find src/ -name "*.py" -exec sed -i.bak 's/\.iteritems()/.items()/g' {} +
find src/ -name "*.py" -exec sed -i.bak 's/\.itervalues()/.values()/g' {} +
find src/ -name "*.py" -exec sed -i.bak 's/\.iterkeys()/.keys()/g' {} +

# Remove .bak files after verifying
find src/ -name "*.bak" -delete
```

### rope — safe automated renaming and refactoring

```python
# pip install rope
from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.refactor.move import create_move

project = Project('.')

# Rename a function/class/variable across the entire project
resource = project.get_resource('mymodule/utils.py')
rename = Rename(project, resource, offset=resource.read().index('old_name'))
changes = rename.get_changes('new_name')
project.do(changes)

project.close()
```

### Bulk fix with AST (for complex transformations)

```python
import ast, astor  # pip install astor

class FixIterItems(ast.NodeTransformer):
    """Replace .iteritems() → .items() etc."""
    RENAME = {'iteritems': 'items', 'itervalues': 'values', 'iterkeys': 'keys'}

    def visit_Call(self, node):
        self.generic_visit(node)
        if (isinstance(node.func, ast.Attribute) and
                node.func.attr in self.RENAME):
            node.func.attr = self.RENAME[node.func.attr]
        return node

import pathlib
for path in pathlib.Path('src').rglob('*.py'):
    source = path.read_text()
    try:
        tree = ast.parse(source)
        new_tree = FixIterItems().visit(tree)
        new_source = astor.to_source(new_tree)
        path.write_text(new_source)
    except SyntaxError:
        print(f"Skipping {path} — syntax error")
```

## Refactoring Legacy Research Code

Common issues in old scientific scripts and how to fix them:

```python
# 1. Magic numbers → named constants
# BAD
result = value * 1.60934
# GOOD
KM_PER_MILE = 1.60934
result = value * KM_PER_MILE

# 2. Positional DataFrame column access → named access
# BAD
name = row[0]; age = row[1]
# GOOD
name = row['name']; age = row['age']

# 3. Hardcoded file paths → configurable
# BAD
df = pd.read_csv('/home/user/data/raw/2024_data.csv')
# GOOD — use pathlib and pass paths as parameters
from pathlib import Path
DATA_DIR = Path(__file__).parent / 'data'
df = pd.read_csv(DATA_DIR / 'raw/2024_data.csv')

# 4. print-based debugging → logging
# BAD
print("Processing", n, "records...")
# GOOD
import logging
log = logging.getLogger(__name__)
log.info("Processing %d records", n)

# 5. Nested loops over DataFrames → vectorized
# BAD
for i in range(len(df)):
    for j in range(len(df2)):
        if df.iloc[i]['id'] == df2.iloc[j]['id']:
            df.at[i, 'value'] = df2.iloc[j]['value']
# GOOD
df = df.merge(df2[['id', 'value']], on='id', how='left', suffixes=('', '_new'))
df['value'] = df['value_new'].fillna(df['value'])
df.drop(columns=['value_new'], inplace=True)
```

## Dead Code Removal

```bash
# vulture — find unused code
pip install vulture
vulture src/                        # list unused functions, classes, variables
vulture src/ --min-confidence 80   # only high-confidence dead code

# Find unused imports (ruff covers this too)
ruff check --select F401 .
```

## Checklist for Legacy Codebase Cleanup

```
1. [ ] Run pyupgrade to modernize syntax
2. [ ] Run ruff --fix for auto-fixable issues
3. [ ] Run black / ruff format for consistent style
4. [ ] Run isort for import ordering
5. [ ] Run vulture to find dead code
6. [ ] Fix bare excepts
7. [ ] Fix mutable default arguments
8. [ ] Replace print debugging with logging
9. [ ] Replace hardcoded paths with pathlib
10. [ ] Replace row-by-row DataFrame loops with vectorized ops
11. [ ] Add type hints to function signatures (use pyright or mypy to check)
```
