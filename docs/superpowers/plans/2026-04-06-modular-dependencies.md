# Modular Dependency Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the project's dependency management to a modular "extras" model and update the setup CLI to selectively install skills based on available dependencies.

**Architecture:** Restructure `pyproject.toml` into functional extras groups, remove all lazy imports/exception-swallowing in the core code, and enhance `setup_skills.py` with an internal dependency-to-skill mapping.

**Tech Stack:** Python (Setuptools), `importlib.util`.

---

### Task 1: Refactor `pyproject.toml` Dependencies

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Replace the `dependencies` list with the core set**

Replace lines 19-70 of `pyproject.toml` with:
```toml
dependencies = [
    "numpy",
    "pandas",
]
```

- [ ] **Step 2: Implement the `optional-dependencies` section**

Add after the `dependencies` block:
```toml
[project.optional-dependencies]
ml = [
    "torch",
    "transformers",
    "datasets",
    "evaluate",
    "accelerate",
    "timm",
    "scipy",
    "scikit-learn",
]
viz = [
    "matplotlib",
    "seaborn",
    "plotly",
    "kaleido",
    "dash",
]
geo = [
    "geopandas",
    "folium",
    "mapclassify",
    "pyarrow",
    "geoalchemy2",
    "contextily",
    "cartopy",
]
db = [
    "sqlalchemy",
    "psycopg2-binary",
    "oracledb",
    "alembic",
    "boto3",
    "s3fs",
]
dict = [
    "pdfplumber",
    "python-docx",
    "python-pptx",
    "extract-msg",
    "easyocr",
    "pdf2image",
    "PyPDF2",
    "pymupdf",
    "defusedxml",
    "openpyxl",
    "pydantic",
    "pydantic-settings",
    "tqdm",
    "click",
]
dev = [
    "pytest",
    "ruff",
    "black",
    "isort",
    "pyupgrade",
    "pylint",
    "vulture",
]
all = [
    "numpy",
    "pandas",
    "torch",
    "transformers",
    "datasets",
    "evaluate",
    "accelerate",
    "timm",
    "scipy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "plotly",
    "kaleido",
    "dash",
    "geopandas",
    "folium",
    "mapclassify",
    "pyarrow",
    "geoalchemy2",
    "contextily",
    "cartopy",
    "sqlalchemy",
    "psycopg2-binary",
    "oracledb",
    "alembic",
    "boto3",
    "s3fs",
    "pdfplumber",
    "python-docx",
    "python-pptx",
    "extract-msg",
    "easyocr",
    "pdf2image",
    "PyPDF2",
    "pymupdf",
    "defusedxml",
    "openpyxl",
    "pydantic",
    "pydantic-settings",
    "tqdm",
    "click",
]
```

- [ ] **Step 3: Commit the changes**

```bash
git add pyproject.toml
git commit -m "feat: modularize dependencies in pyproject.toml"
```

---

### Task 2: Remove Lazy Imports in Dictionary Agent

**Files:**
- Modify: `src/dictionary_agent/extractor.py`
- Modify: `src/dictionary_agent/ocr_engine.py`

- [x] **Step 1: Standardize imports in `extractor.py`**

Replace:
```python
try:
    from pyOneNote.Main import OneDocment
except ImportError:
    OneDocment = None
```
With:
```python
from pyOneNote.Main import OneDocment
```

- [x] **Step 2: Standardize imports in `ocr_engine.py`**

Replace the top-level lazy variables and functions with:
```python
import easyocr
import pdf2image
import numpy as np
```
Update `extract_text_via_ocr` to use `easyocr.Reader(['he', 'en'])` and `pdf2image` directly.

- [x] **Step 3: Commit the changes**

```bash
git add src/dictionary_agent/extractor.py src/dictionary_agent/ocr_engine.py
git commit -m "refactor: remove lazy imports and standardise top-level imports"
```

---

### Task 3: Dependency-Aware Skill Setup

**Files:**
- Modify: `src/claude_data_skills/cli/setup_skills.py`

- [ ] **Step 1: Implement the dependency check logic**

Add mapping to `src/claude_data_skills/cli/setup_skills.py`:
```python
SKILL_DEPENDENCIES = {
    "machine-learning": ["torch", "transformers"],
    "visualization": ["matplotlib", "plotly"],
    "data-analysis/geopandas": ["geopandas"],
    "data-sources/database-pro": ["sqlalchemy"],
    "unstructured-data-processing": ["pdfplumber", "docx", "pptx", "extract_msg"],
}

def is_skill_ready(skill_rel_path):
    """Checks if all dependencies for a given skill path are installed."""
    for skill_prefix, pkgs in SKILL_DEPENDENCIES.items():
        if skill_rel_path.startswith(skill_prefix):
            for pkg in pkgs:
                if importlib.util.find_spec(pkg) is None:
                    return False, pkg
    return True, None
```

- [ ] **Step 2: Update `copy_skills_to_claude_home` to filter directories**

Modify the copying loop to call `is_skill_ready(rel_path)` before copying each skill directory.

- [ ] **Step 3: Commit the changes**

```bash
git add src/claude_data_skills/cli/setup_skills.py
git commit -m "feat: implement dependency-aware skill setup"
```

---

### Task 4: Final Verification

- [ ] **Step 1: Run the setup script**
- [ ] **Step 2: Verify copied skills in ~/.claude/skills**
- [ ] **Step 3: Confirm dictionary agent error behavior**
