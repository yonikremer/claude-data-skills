# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is **claude-data-analytics-skills**, a personalized Claude Code plugin containing high-quality skills for data science, machine learning, research, and engineering. It is specifically optimized for use with **Open-Source LLMs**, emphasizing resource-aware execution, idiomatic Python best practices, and robust visualization via Plotly.

## Releasing

To release a new version:
1. Bump the `version` field in `.claude-plugin/marketplace.json`
2. Commit and push to `main`

## Architecture

### Plugin Entry Point

`.claude-plugin/marketplace.json` — registers the plugin and lists all skill paths.

### Skill Structure

Each skill lives under `skills/` and follows this pattern:

```
skills/<skill-name>/
├── SKILL.md              # Required: entry point loaded by Claude Code
├── references/           # Optional: supplementary reference docs loaded on demand
│   └── *.md
└── scripts/              # Optional: executable Python/shell scripts
```

### Gold Standard Requirements

Every skill in this repository should adhere to the "Gold Standard":
1. **Data Integrity & Safety**: **NEVER** delete, overwrite, or drop data (files, columns, or rows) without explicit user permission. Prefer creating new columns or files (e.g., `_processed.csv`) to preserve original data.
2. **Resource Awareness**: Call `get-available-resources` for data-intensive tasks.
3. **Strict Idioms**: Enforce PEP-8 and modern library syntax (e.g., Pandas 2.0+, Pydantic V2).
4. **Reference Tiering**: Keep `SKILL.md` focused; move deep documentation to `references/`.
5. **Pitfalls Section**: Explicitly list common hallucinations or errors for OS models.

### Special Skills

- **`get-available-resources`**: Detects CPU/GPU/memory/disk info.
- **`python-best-practices`**: Enforces coding standards and tiered testing strategy.
- **`exploratory-data-analysis`**: Entry point for scientific file analysis.
