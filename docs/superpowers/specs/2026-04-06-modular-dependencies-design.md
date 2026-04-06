# Design Spec: Modular Dependency Management for Claude Data Skills

**Date:** 2026-04-06
**Status:** Approved
**Topic:** Modularizing the project's dependencies to allow for faster installation and lightweight core usage.

---

## 1. Problem Statement
The current `pyproject.toml` forces a massive installation of over 50 dependencies (ML, GIS, Visualization, Database tools, etc.). Many users only need a subset of these features, but are forced to wait for all of them to install. Additionally, the project lacks a clear "core" definition and has several missing dependencies (e.g., `python-docx`, `extract-msg`) that are used in the code but not listed in the metadata.

## 2. Goals
- **Lightweight Core:** The base installation (`pip install .`) should only include `numpy` and `pandas`.
- **Modular Extras:** All heavy or specialized libraries should be moved to optional "extras" (e.g., `ml`, `viz`, `geo`, `db`, `dict`).
- **Selective Skill Setup:** The `setup-data-skills` CLI command should only copy skills to the user's home directory if their dependencies are met in the current environment.
- **No Lazy Imports:** The code should use standard, top-level imports. If a library is missing, the user should see a `ModuleNotFoundError` when they attempt to use that feature, encouraging them to install the relevant extra.

## 3. Architecture

### 3.1. Dependency Groups (`pyproject.toml`)

| Group | Dependencies |
| :--- | :--- |
| **Core (Base)** | `numpy`, `pandas` |
| **`ml`** | `torch`, `transformers`, `datasets`, `evaluate`, `accelerate`, `timm`, `scipy`, `scikit-learn` |
| **`viz`** | `matplotlib`, `seaborn`, `plotly`, `kaleido`, `dash` |
| **`geo`** | `geopandas`, `folium`, `mapclassify`, `pyarrow`, `geoalchemy2`, `contextily`, `cartopy` |
| **`db`** | `sqlalchemy`, `psycopg2-binary`, `oracledb`, `alembic`, `boto3`, `s3fs` |
| **`dict`** | `pdfplumber`, `python-docx`, `python-pptx`, `extract-msg`, `easyocr`, `pdf2image`, `PyPDF2`, `pymupdf`, `defusedxml`, `openpyxl`, `pydantic`, `pydantic-settings`, `tqdm`, `click` |
| **`dev`** | `pytest`, `ruff`, `black`, `isort`, `pyupgrade`, `pylint`, `vulture` |
| **`all`** | All of the above |

### 3.2. Code Cleanup (Standardizing Imports)
All `try/except ImportError` blocks and lazy imports inside functions (e.g., in `src/dictionary_agent/ocr_engine.py` and `src/dictionary_agent/extractor.py`) will be removed and replaced with standard top-level imports.

### 3.3. Enhanced Setup Logic (`src/claude_data_skills/cli/setup_skills.py`)
The `copy_skills_to_claude_home` function will be updated to:
1. Define a mapping between skill directories and their required packages.
2. Check if the required package is installed using `importlib.util.find_spec()`.
3. Only copy skill directories that have all their requirements met.
4. Report which skills were skipped due to missing dependencies.

## 4. User Experience
- **Installation:**
  - `pip install .` (Fastest, core only)
  - `pip install ".[ml,viz]"` (Install specific modules)
  - `pip install ".[all]"` (Full installation)
- **Usage:**
  - If a user tries to run a command (like `dictionary-scan`) without the `dict` extra, Python will throw a `ModuleNotFoundError`.
  - The `setup-data-skills` command will only install the tools the user is actually ready to use.

## 5. Success Criteria
- Base installation finishes in seconds.
- `pip install .` results in a working environment with only `numpy` and `pandas`.
- `setup-data-skills` correctly filters the skills copied to `~/.claude/skills`.
- No more lazy import logic or `try/except` blocks in the codebase.
