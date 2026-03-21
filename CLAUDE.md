# claude-data-skills

A personal collection of Claude Code skills for commercial data research and analysis.
Maintained by @yonikremer. Public but personal — no bio, med, physics, or public dataset skills.

## What's in This Repo

Skills are organized under `skills/`. Each skill is a folder with a `SKILL.md` and optional
`scripts/` and `references/` subdirectories.

### Data Analysis & Querying
- **analyze** — Ad-hoc data questions, statistical analysis, EDA on private datasets
- **explore-data** — Profile a dataset's shape, types, nulls, distributions, and anomalies
- **write-query** — Optimized SQL with dialect-specific best practices
- **build-dashboard** — Interactive HTML dashboards with filters and charts
- **create-viz** — Python visualizations (matplotlib/seaborn/plotly), publication-quality
- **validate** — Pre-delivery QA: catch survivorship bias, incorrect aggregations, type errors
- **sqlite** — SQLite-specific queries, indexing, and optimization
- **postgresql** — PostgreSQL best practices, window functions, EXPLAIN plans, indexing
- **oracle** — Oracle SQL conventions: ROWNUM, CONNECT BY, bind variables, hints
- **elasticsearch** — Elasticsearch query DSL, aggregations, index mapping, search optimization

### File Formats
- **csv** — Parse, clean, and analyze CSV/TSV files including malformed inputs
- **excel** (xlsx) — Spreadsheet manipulation: formulas, charts, data transformations
- **pdf** — Extract text, tables, and metadata from PDFs
- **json** — Parse, validate, and transform JSON/JSONL with schema enforcement
- **audio** — Audio metadata extraction, waveform analysis, feature extraction

### ML & Modeling
- **scikit-learn** — Classification, regression, clustering, preprocessing pipelines
- **timeseries** — Time series forecasting, decomposition, anomaly detection
- **xgboost** — Gradient boosting for tabular data, hyperparameter tuning
- **error-analysis** — Systematically identify and categorize model failure modes

### Utilities
- **generate-synthetic-data** — Create realistic synthetic data for testing pipelines
- **pptx** — Generate data-driven slide decks programmatically

## Releasing

Releases are automated via GitHub Actions (`.github/workflows/release.yml`).
To release: bump `version` in `.claude-plugin/marketplace.json`, commit to `main`.
No build step, test suite, or linting.

## Plugin Entry Point

`.claude-plugin/marketplace.json` registers the plugin and lists all skill paths.
Every new skill must be added here to be distributed.

## Skill Structure

```
skills/<skill-name>/
├── SKILL.md              # Required: YAML frontmatter + instructions
├── references/           # Optional: loaded on demand, no context cost until read
│   └── *.md
└── scripts/              # Optional: Python/shell scripts executed via bash
```

## SKILL.md Frontmatter Template

```yaml
---
name: skill-name
description: >
  One precise sentence on what this skill does. Then: "Use when [trigger conditions].
  Do NOT use when [anti-cases — name the correct alternative skill instead]."
license: MIT
metadata:
    skill-author: yonikremer
---
```

The `description` is the only field Claude reads at startup (~100 tokens per skill).
Make it unambiguous — Claude picks from all installed skills based on this alone.

## Hard Rules

- All data is private and commercial — never suggest public datasets or external APIs
- Always use `polars` over `pandas` for dataframe work
- Always use `orjson` for JSON serialization
- Use `uv` for package management — never raw `pip`
- Use `logger.error` not `print` for error reporting
- Never ingest more than 10 rows of a dataframe into context at once
- Use `pathlib.Path` everywhere — no hardcoded string paths
- Type hints on all function signatures
- Line length: 88 chars (ruff standard)
