# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is **claude-scientific-skills**, a Claude Code plugin by K-Dense Inc. containing 150+ skills for scientific computing, data analysis, bioinformatics, cheminformatics, machine learning, and research workflows. It is distributed via the Claude Code plugin marketplace.

## Releasing

Releases are fully automated via GitHub Actions (`.github/workflows/release.yml`). To release a new version:
1. Bump the `version` field in `.claude-plugin/marketplace.json`
2. Commit and push to `main` — the workflow auto-creates a GitHub Release with a changelog

There is no build step, test suite, or linting configuration in this repository.

## Architecture

### Plugin Entry Point

`.claude-plugin/marketplace.json` — registers the plugin and lists all skill paths. Every new skill must be added here to be distributed.

### Skill Structure

Each skill lives under `scientific-skills/<skill-name>/` and follows this pattern:

```
scientific-skills/<skill-name>/
├── SKILL.md              # Required: entry point loaded by Claude Code
├── references/           # Optional: supplementary reference docs loaded on demand
│   └── *.md
└── scripts/              # Optional: executable Python/shell scripts
```

### SKILL.md Format

Every `SKILL.md` must have YAML frontmatter:

```yaml
---
name: skill-name
description: One-liner used for skill matching/routing — be precise about when to use vs. alternatives
license: https://...
metadata:
    skill-author: K-Dense Inc.
---
```

The `description` field is critical — it determines when Claude activates the skill. Reference documentation in `references/` is loaded on demand within the skill (e.g., "For details, load `references/core_concepts.md`").

### Skill Categories

- **Library skills**: Wrap a Python package (polars, dask, matplotlib, scikit-learn, etc.)
- **Database skills**: Provide access patterns for scientific databases (PubMed, ChEMBL, UniProt, etc.)
- **Workflow skills**: Orchestrate multi-step scientific processes (EDA, peer-review, scientific-writing, etc.)
- **Integration skills**: Connect to external platforms (Benchling, DNAnexus, Opentrons, etc.)
- **Output skills**: Generate documents (docx, pdf, pptx, xlsx, latex-posters, etc.)

### Special Skills

- **`get-available-resources`**: Should be triggered at the start of any computationally intensive task. Runs `scripts/detect_resources.py` → writes `.claude_resources.json` with CPU/GPU/memory/disk info and recommendations.
- **`exploratory-data-analysis`**: General-purpose EDA entry point.
