# Agent Guide: claude-data-skills

This file is a single source of truth for AI coding agents working in this repository. The reader is assumed to know nothing about the project. All statements below are derived from the actual files in the working tree; assumptions have been avoided.

## 1. Project Overview

**claude-data-skills** is a professional-grade Python package and skill library for AI-assisted data science, machine learning, research, and engineering workflows. It ships on PyPI as `claude-data-skills`.

- **Package name on PyPI:** `claude-data-skills`
- **Local package name:** `claude_data_skills`
- **Author:** Yoni Kremer
- **License:** MIT
- **Python requirement:** >= 3.9
- **Current declared version:** `3.5.0` in `pyproject.toml`; `3.5.2` in `src/claude_data_skills/__version__.py`; `3.0.0` in `.claude-plugin/marketplace.json`. These are intentionally noted as divergent.

The project has two distinct products:

1. **A pip-installable Python package** (`src/claude_data_skills/`) that provides a setup CLI and a small set of executable scripts.
2. **A skill library** (`src/skills/`) — a collection of markdown-based AI agent skills (`SKILL.md` files) and runnable Python reference scripts. After installation, `setup-data-skills` copies the skill library to `~/.claude/skills` and Gemini-compatible slash-command wrappers to `.gemini/commands`.

### What the project is NOT

- It is not a monolithic application. Most of the repository is documentation and reference scripts rather than a single runtime service.
- It does not contain a running web server or API by default.
- The GraphRAG/dictionary-agent subsystem is documented and referenced, but its Python source files are not present in the working tree (only compiled `__pycache__` artifacts remain). See Section 5.

## 2. Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.9+ |
| Build backend | `setuptools` with `pyproject.toml` |
| Package layout | `src/` layout (`package-dir = {"" = "src"}`) |
| Core runtime deps | `numpy`, `pandas` |
| Optional dep groups | `ml`, `viz`, `geo`, `db`, `dev`, `all` |
| Linting / formatting | `ruff`, `black`, `isort`, `pylint`, `vulture`, `pyupgrade` |
| Testing | `pytest` |
| CLI entry points | `stdlib-demo`, `setup-data-skills` |
| Environment notes | Developed on Windows; `Bash` tool runs Git Bash |

### Optional dependency groups

- `ml`: PyTorch, Hugging Face (`transformers`, `datasets`, `evaluate`, `accelerate`, `timm`), `scipy`, `scikit-learn`
- `viz`: `matplotlib`, `seaborn`, `plotly`, `kaleido`, `dash`
- `geo`: `geopandas`, `folium`, `mapclassify`, `pyarrow`, `geoalchemy2`, `contextily`, `cartopy`
- `db`: `sqlalchemy`, `psycopg2-binary`, `oracledb`, `alembic`, `boto3`, `s3fs`
- `dev`: `pytest`, `ruff`, `black`, `isort`, `pyupgrade`, `pylint`, `vulture`
- `all`: Union of the above (except `dev`)

## 3. Repository Layout

```text
.
├── pyproject.toml              # Build metadata, deps, entry points, ruff config
├── publish.ps1                 # PowerShell release automation for PyPI
├── MANIFEST.in                 # Package inclusion rules
├── package-lock.json           # Empty npm lockfile (no Node dependencies)
├── README.md                   # User-facing overview
├── CLAUDE.md                   # Legacy Claude Code guidance (still partly accurate)
├── GEMINI.md                   # Gemini/GraphRAG integration notes
├── SKILLS.md                   # Catalog of all skills
├── GOLDEN_TERMS.md             # Domain dictionary (currently empty)
├── RUNNING_INSTRUCTIONS.md     # GraphRAG/dictionary-agent usage guide
├── TODO.md                     # Roadmap
├── src/
│   ├── claude_data_skills/     # Installable Python package
│   │   ├── __init__.py         # Exposes __version__
│   │   ├── __version__.py      # Single source of version string
│   │   ├── cli/
│   │   │   └── setup_skills.py # setup-data-skills entry point
│   │   └── commands/           # Gemini slash-command .toml wrappers
│   ├── skills/                 # Skill library (markdown + scripts)
│   │   ├── commands/           # Claude slash-command wrappers
│   │   ├── core-workflow/      # Brainstorming, TDD, debugging, planning, verification
│   │   ├── data-analysis/      # NumPy, Pandas, Polars, EDA, geopandas, statsmodels
│   │   ├── data-sources/       # SQL, SQLAlchemy, Elasticsearch, S3
│   │   ├── infrastructure-tools/  # Resources, validation, git, gitlab, jupyter, windows-cli
│   │   ├── learning-and-skill-building/  # tech-explorer, writing-skills, API/DB skill creators
│   │   ├── machine-learning/   # Classical ML, deep learning, PyMC, RL, TimesFM
│   │   ├── networking-security/# Logs, networks, scapy, Wireshark
│   │   ├── python-dev/         # Python core pro, legacy migration, debugging, dotenv
│   │   ├── scientific-workflow/  # Scientific research suite
│   │   ├── unstructured-data-processing/  # Documents, binary parsing, ECC, ffmpeg, shapely
│   │   ├── visualization/      # Plotly, Dash, Seaborn
│   │   └── web-scraping/
│   └── dictionary_agent/       # Documented GraphRAG subsystem (source .py files missing)
├── tests/                      # Minimal test suite
│   └── cupy_signal_explorer/   # Cupy/SciPy signal-processing checks
├── scripts/
│   └── doc_extractor.py        # CLI helper to print docstrings for dotted paths
├── docs/
│   └── ARCHITECTURE_GRAPH_RAG.md
└── storage/
    └── hashes.json
```

## 4. Skill Conventions

Each skill lives in its own directory under `src/skills/` and follows a standardized structure.

### Required frontmatter

Every `SKILL.md` begins with YAML frontmatter:

```yaml
---
name: <skill-name>
description: Use when... <short trigger description>
---
```

The `description` is optimized for agent discovery: it starts with "Use when...".

### Common subdirectories

- `references/` — Deep API references, extracted docstrings, or advanced patterns.
- `scripts/` — Runnable Python examples and helper scripts.
- `assets/` — Templates, notebooks, or model files.

### Slash commands

The `src/skills/commands/` directory contains thin skill wrappers that map to slash commands:

| Command | Skill invoked |
|---------|---------------|
| `/analyze <file>` | `exploratory-data-analysis` |
| `/plot <type> <file>` | `visualization-pro` |
| `/query <task>` | `database-pro` |
| `/model <target> <file>` | `ml-classical` |
| `/forecast <col> <file>` | `timesfm-forecasting` |
| `/explore <technology>` | `tech-explorer` |

The Gemini CLI receives copies of these wrappers via `setup-data-skills`.

## 5. Known State Issues / Caveats

Before editing, be aware of the following discrepancies in the working tree.

### 5.1 Version drift

- `pyproject.toml` declares `3.5.0`
- `src/claude_data_skills/__version__.py` declares `3.5.2`
- `.claude-plugin/marketplace.json` declares `3.0.0`

If you are asked to release, reconcile these first. The release script `publish.ps1` updates `__version__.py` and `pyproject.toml` but does not touch `marketplace.json`.

### 5.2 Missing dictionary_agent source files

`src/dictionary_agent/` contains only `__pycache__/` artifacts. The original `.py` modules (`pipeline.py`, `graph_engine.py`, `tools.py`, `storage.py`, etc.) referenced in `RUNNING_INSTRUCTIONS.md`, `docs/ARCHITECTURE_GRAPH_RAG.md`, and `GEMINI.md` are not present. Do not assume the GraphRAG pipeline can be run from source without restoring those files.

### 5.3 .gitignore quirks

`.gitignore` lists `pyproject.toml`, `.claude/`, `.python-version`, `uv.lock`, `main.py`, and `scan_skills.py` as ignored. This is unusual. Any work that creates or modifies those files must be explicit; otherwise they may be excluded from version control.

### 5.4 Test coverage is narrow

The only test files are under `tests/cupy_signal_explorer/` and require `cupy`. There is no broad unit-test coverage for the skill library or CLI.

## 6. Build, Install, and Test Commands

### Local editable install

```bash
pip install -e .
```

### Install with optional extras

```bash
pip install -e ".[dev]"
pip install -e ".[all]"
pip install -e ".[ml,viz]"
```

### Run the setup CLI (copies skills to `~/.claude/skills` and `.gemini/commands`)

```bash
setup-data-skills
```

### Run the stdlib demo

```bash
stdlib-demo
```

### Run tests

```bash
pytest
```

Note: The `cupy_signal_explorer` tests require a working CuPy installation and a compatible NVIDIA GPU.

### Lint and format

The project configures `ruff` in `pyproject.toml`:

```bash
ruff check .
ruff format .
```

Other tools listed in `dev` dependencies and commonly used:

```bash
black src tests
isort src tests
pylint src
vulture src
pyupgrade --py39-plus <files>
```

### Build and publish (Windows/PowerShell)

```powershell
.\publish.ps1 -VersionType patch   # or minor / major
```

This script:
1. Reads `src/claude_data_skills/__version__.py`
2. Bumps the version
3. Updates both `__version__.py` and `pyproject.toml`
4. Installs `build` and `twine`
5. Cleans and rebuilds `dist/`
6. Uploads to PyPI using stored credentials

## 7. Code Style Guidelines

The repository expects modern, idiomatic Python. The following rules are repeated across the skill documentation and should be honored in any new code.

### 7.1 General Python style

- Target Python 3.9+.
- Follow PEP 8. Line length is configured to 88 characters for `ruff`.
- Use `pathlib.Path` instead of `os.path`.
- Use context managers (`with`) for file I/O, sessions, and connections.
- Prefer f-strings for formatting.
- Add type hints to function signatures.
- Avoid mutable default arguments; use `None` and initialize inside the function.
- Avoid bare `except:` blocks. Never silently catch `ImportError`; fail loudly so missing dependencies are obvious.
- Use atomic write patterns (write to a temp file, then `replace`) for file mutations.

### 7.2 Data safety rules

These are treated as mandatory guardrails:

- **Never delete, overwrite, or drop data** (files, columns, rows) without explicit user permission. Prefer creating new artifacts (e.g., `_processed.csv`).
- **Atomic writes** for all file output.
- **Resource awareness**: For data loading over ~100 MB or model training, invoke or mirror the behavior of `get-available-resources` first.
- **No silent import failures**: Missing dependencies must raise clearly.

### 7.3 Skill authoring

When creating or editing a skill:

- Start `SKILL.md` with `name` and `description: Use when...` frontmatter.
- Include mandatory pre-flight checks where relevant (resource detection, schema validation).
- Keep `SKILL.md` focused; move deep references to `references/`.
- Include a "Wall of Shame" / pitfalls section for common hallucinations or anti-patterns.
- Add runnable example scripts in `scripts/` when practical.

## 8. Testing Instructions

- The test runner is `pytest`.
- Tests live in `tests/`.
- Current tests are GPU-specific (`tests/cupy_signal_explorer/`). They will fail or be skipped if `cupy` and CUDA are unavailable.
- When adding new code, add corresponding `pytest` tests. Prefer fixtures and parametrization.
- Before claiming a task is complete, run the tests that cover your change and inspect the output.

## 9. Security Considerations

- The GraphRAG/dictionary-agent subsystem is designed to run on private local models (Ollama/vLLM) so internal document content is not sent to external APIs. Because the source files are missing, this security model currently cannot be exercised.
- Do not commit credentials, `.env` files, or internal document content.
- The `.gitignore` already excludes `.env` and build artifacts, but note that it also excludes `pyproject.toml` and `.claude/`. Double-check what is tracked before relying on the ignore file.
- The publish script uploads to PyPI using credentials from `~/.pypirc` or environment variables (`TWINE_USERNAME`, `TWINE_PASSWORD`, `TWINE_API_KEY`). Do not run it unless explicitly authorized.

## 10. Deployment / Release Process

1. Decide the version bump type (`patch`, `minor`, `major`).
2. Run `.\publish.ps1 -VersionType <type>`.
3. The script updates `src/claude_data_skills/__version__.py` and `pyproject.toml`, builds a wheel and sdist, and uploads to PyPI.
4. Manually reconcile `.claude-plugin/marketplace.json` if the plugin marketplace entry must also change.
5. There is no CI/CD pipeline in this repository; releases are performed locally from the `main` branch.

## 11. Quick Reference for Agents

- **Need to add a skill?** Create a directory under `src/skills/` with `SKILL.md`, optionally `references/` and `scripts/`.
- **Need to add a CLI command?** Add an entry point in `pyproject.toml` and implement it under `src/claude_data_skills/cli/` or `src/claude_data_skills/commands/` for Gemini wrappers.
- **Need to change the version?** Update `src/claude_data_skills/__version__.py` and `pyproject.toml` together; consider `marketplace.json`.
- **Need to run the GraphRAG pipeline?** First restore the missing `src/dictionary_agent/*.py` source files; only compiled bytecode remains.
- **Need to verify your changes?** Run `pytest`, `ruff check .`, and `ruff format .`.
