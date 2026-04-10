# Graph-Sieve Standalone Package Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract `dictionary_agent` from `claude-data-skills` into a new repository called `graph-sieve`, turning it into a standalone utility/service.

**Architecture:** The extraction moves all extraction, OCR, and graph-engine logic into a new package named `graph_sieve`. This package will expose its functionality via CLI entry points, an MCP server, and a Gemini slash command.

**Tech Stack:** Python 3.9+, Pydantic, easyocr, pdfplumber, mcp (Model Context Protocol).

---

### Task 1: Setup New `graph-sieve` Package Structure

**Files:**
- Create: `graph-sieve/pyproject.toml`
- Create: `graph-sieve/src/graph_sieve/__init__.py`
- Create: `graph-sieve/.gemini/commands/define.toml`

- [ ] **Step 1: Create `pyproject.toml` for the new package**

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "graph-sieve"
version = "1.0.0"
description = "Full Spectrum Graph Sieve - Automated Technical Term Extraction and Relationship Mapping"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
dependencies = [
    "pdfplumber",
    "python-docx",
    "python-pptx",
    "extract-msg",
    "markitdown",
    "easyocr",
    "pdf2image",
    "PyPDF2",
    "pymupdf",
    "pydantic",
    "pydantic-settings",
    "tqdm",
    "click",
    "mcp",
    "numpy",
    "pandas",
]

[project.scripts]
graph-sieve-scan = "graph_sieve.run_scanner:main"
graph-sieve-lookup = "graph_sieve.tools:main"
graph-sieve-mcp = "graph_sieve.mcp_server:mcp.run"
graph-sieve-visualize = "graph_sieve.visualize:main"
graph-sieve-whois = "graph_sieve.whois:main"

[tool.setuptools]
package-dir = { "" = "src" }
```

- [ ] **Step 2: Create `src/graph_sieve/__init__.py`**

```python
__version__ = "1.0.0"
```

- [ ] **Step 3: Move and update `.gemini/commands/define.toml`**

```toml
description = "Lookup a technical term in the dictionary"
prompt = """
Use the `lookup_term` tool from `graph_sieve.tools` to find the definition and context for: {{args}}.
If found, explain how it relates to the current task. If not found, check the Golden Terms or ask for clarification.
"""
```

### Task 2: Migrate Core Logic and Rename Imports

**Files:**
- Create: `graph-sieve/src/graph_sieve/*.py` (migrated from `src/dictionary_agent/`)

- [ ] **Step 1: Copy all files from `src/dictionary_agent/` to `graph-sieve/src/graph_sieve/`**
- [ ] **Step 2: Rename all internal imports from `dictionary_agent` to `graph_sieve`**

Example for `agent.py`:
```python
# Old
from dictionary_agent.extractor import extract_terms
# New
from graph_sieve.extractor import extract_terms
```

### Task 3: Migrate and Verify Tests

**Files:**
- Create: `graph-sieve/tests/*.py` (migrated from `tests/dictionary_agent/`)

- [ ] **Step 1: Copy tests from `tests/dictionary_agent/` to `graph-sieve/tests/`**
- [ ] **Step 2: Update test imports to use `graph_sieve`**
- [ ] **Step 3: Run tests to ensure everything works in isolation**

Run: `pytest graph-sieve/tests/`
Expected: ALL PASS

### Task 4: Cleanup `claude-data-skills` Repository

**Files:**
- Modify: `pyproject.toml`
- Delete: `src/dictionary_agent/`
- Delete: `tests/dictionary_agent/`
- Delete: `src/skills/unstructured-data-processing/dictionary-agent/`
- Delete: `.gemini/commands/define.toml`

- [ ] **Step 1: Remove dictionary-related entries from `pyproject.toml`**
- [ ] **Step 2: Delete migrated directories**
- [ ] **Step 3: Verify `claude-data-skills` still builds/runs (without dictionary features)**

### Task 5: Update Documentation

**Files:**
- Modify: `GEMINI.md`
- Modify: `SKILLS.md`
- Modify: `README.md`
- Create: `graph-sieve/README.md`

- [ ] **Step 1: Update `GEMINI.md` to reference `graph-sieve` as an external dependency**
- [ ] **Step 2: Update `SKILLS.md` to remove the `dictionary-agent` skill**
- [ ] **Step 3: Create a comprehensive `README.md` for `graph-sieve`**
- [ ] **Step 4: Final verification and commit**
