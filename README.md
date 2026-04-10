# Claude Data Skills 🐍📊

A professional-grade collection of data science, analysis, and engineering skills and scripts for AI-assisted
development.

[![PyPI Version](https://img.shields.io/pypi/v/claude-data-skills.svg)](https://pypi.org/project/claude-data-skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

`claude-data-skills` is a comprehensive library designed to enhance AI-assisted data workflows. It provides a structured
collection of "skills"—reusable, idiomatic patterns and scripts for everything from advanced standard library usage to
complex machine learning pipelines and professional development workflows.

## Key Features

- **🚀 Professional Python Core**: Unified expert guide for PEP-8, Pydantic, Pytest, and high-performance parallelism.
- **📊 Data Analysis Pro**: Consolidated power-user guide for NumPy, Pandas, and Polars. Unified strategy for scaling
  from KB to 100GB+.
- **🕸️ Full Spectrum Graph Sieve (GraphRAG)**: Advanced agentic workflow for extracting relationship-aware domain knowledge from internal docs (.docx, .one, .msg, .pdf). Now powered by the external [graph-sieve](https://github.com/your-org/graph-sieve) package.
- **⚡ Superpowers Workflow**: Integrated skills for brainstorming, TDD, systematic debugging, and plan execution.
- **🛡️ Data Safety First**: Built-in guardrails to prevent accidental data loss or corruption during autonomous
  execution.
- **📈 Visualization Pro**: Expert guide for Plotly (interactive), Dash (dashboards), and Seaborn (static stats).
- **🗄️ Database Pro**: Unified access for SQL (Postgres), SQLAlchemy (ORM), Elasticsearch, and S3.
- **📁 Document Processing Pro**: Consolidated expert guide for PDF, Word (DOCX), Excel (XLSX), and PowerPoint (PPTX).
- **🔬 Scientific Research Suite**: Unified guide for the entire scientific lifecycle: brainstorming, writing (IMRAD),
  and peer review.
- **🔄 Legacy Migration Suite**: Specialized patterns for migrating C#, MATLAB, and Python 2 code to modern Python (
  3.9+).

## Installation

Install the package directly from PyPI:

```bash
pip install claude-data-skills
```

## Quick Start

### Post-Installation Setup

After installing the package, run the following command to copy the necessary skills files to your user's Claude home
directory (`~/.claude/skills`):

```bash
setup-claude-skills
```

### Using the CLI

The package includes several built-in commands. For example, to run the standard library demonstration:

```bash
stdlib-demo
```

### Importing Skills

You can import advanced utility patterns directly into your own scripts:

```python
from skills.python_dev.python_stdlib_pro.scripts.stdlib_demo import test_pathlib

# Run a verified pathlib pattern
test_pathlib()
```

## Core Principles

- **Resource Aware**: Every intensive task starts with hardware resource validation.
- **LLM Optimized**: Scripts are dense, idiomatic, and contain strict guardrails for local/open-source LLMs.
- **Atomic Operations**: Prevents file corruption by using temp-and-replace patterns for all writes.

## Project Structure

```text
skills/
├── core-workflow/          # Brainstorming, TDD, Debugging, Plans
├── data-analysis/          # Data Analysis Pro (NumPy, Pandas, Polars), Geopandas
├── data-sources/           # Database Pro (Postgres, SQLAlchemy, ES, S3)
├── machine-learning/       # ML-Classical, ML-Deep-Learning, PyMC
├── python-dev/             # Python Core Pro, Legacy Migration Suite, Logic Recovery
├── scientific-workflow/    # Scientific Research Suite
└── unstructured-data/      # Document Processing Pro, Binary Data Parsing
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created and maintained by **Yoni Kremer**.
