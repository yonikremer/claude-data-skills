# Design Spec: Graph-Sieve Standalone Package Extraction

**Date:** 2026-04-10
**Status:** Draft
**Topic:** Architectural separation of the "Full Spectrum Graph Sieve" from the `claude-data-skills` repository.

## 1. Executive Summary
This design outlines the extraction of the `dictionary_agent` module from the `claude-data-skills` repository into a new, independent Python package named `graph-sieve`. This move transforms a project-specific "skill" into a generic, standalone utility/service capable of providing relationship-aware domain knowledge (GraphRAG) to any AI agent via CLI, MCP, or slash commands.

## 2. Goals & Success Criteria
- **Standalone Package:** `graph-sieve` is installable via standard Python tools (`pip`, `poetry`, etc.) without requiring `claude-data-skills`.
- **Clean Extraction:** No `dictionary_agent` code remains in the original repository.
- **Generic Utility:** The package provides its own entry points, slash commands (`/define`), and MCP server.
- **Backward Compatibility:** Users of `claude-data-skills` can still utilize the dictionary agent by installing `graph-sieve` as a dependency.

## 3. Architecture & Components

### 3.1. Repository Structure (New: `graph-sieve`)
The new repository will follow a modern Python package structure:
```text
graph-sieve/
├── pyproject.toml         # Package metadata, entry points, and dependencies
├── README.md              # Standalone documentation and usage guide
├── .gemini/
│   └── commands/
│       └── define.toml    # Slash command definition for Gemini CLI
├── src/
│   └── graph_sieve/       # Renamed from dictionary_agent
│       ├── __init__.py
│       ├── agent.py       # Core logic
│       ├── graph_engine.py# GraphRAG implementation
│       ├── mcp_server.py  # Model Context Protocol integration
│       └── tools.py       # CLI and lookup utilities
├── tests/                 # Migrated from tests/dictionary_agent/
└── storage/               # Default location for persistent dictionaries
```

### 3.2. Code Migration Mapping
| Original Path (in `claude-data-skills`) | New Path (in `graph-sieve`) |
| :--- | :--- |
| `src/dictionary_agent/` | `src/graph_sieve/` |
| `tests/dictionary_agent/` | `tests/` |
| `src/skills/unstructured-data-processing/dictionary-agent/SKILL.md` | `README.md` (and optional internal `SKILL.md`) |
| `.gemini/commands/define.toml` | `.gemini/commands/define.toml` |

### 3.3. Dependency Management
The `dict` optional-dependency group in `claude-data-skills` will be moved to the core `dependencies` of `graph-sieve`:
- `pdfplumber`, `python-docx`, `python-pptx`, `extract-msg`
- `easyocr`, `pdf2image`, `PyPDF2`, `pymupdf`
- `pydantic`, `pydantic-settings`, `mcp`, `click`, `tqdm`

## 4. Integration Strategy

### 4.1. Slash Commands & MCP
- The `/define` command will be moved to the new repository.
- The command logic will be updated to reference `graph_sieve.tools:lookup_term`.
- The MCP server will be the primary interface for "live" agent integration, allowing any agent to query the graph sieve.

### 4.2. `claude-data-skills` Cleanup
1. **Remove Code:** Delete all files in `src/dictionary_agent/`.
2. **Remove Tests:** Delete all files in `tests/dictionary_agent/`.
3. **Update `pyproject.toml`:**
   - Remove `dictionary-scan`, `dictionary-lookup`, etc., from `project.scripts`.
   - Remove `dict` from `optional-dependencies`.
   - Remove the `dictionary-agent` skill from `src/skills/`.
4. **Update `GEMINI.md`:** Reference `graph-sieve` as an external dependency for domain knowledge lookup.

## 5. Implementation Plan

### Phase 1: Preparation (New Repository)
1. Initialize the `graph-sieve` repository.
2. Create `pyproject.toml` with moved dependencies and entry points.
3. Migrate code from `src/dictionary_agent/` to `src/graph_sieve/` (renaming as needed).
4. Migrate tests and verify they pass in the new environment.

### Phase 2: Tooling Migration
1. Move `.gemini/commands/define.toml` to the new repo.
2. Update the command's prompt to use the new package name.
3. Verify the MCP server works independently.

### Phase 3: Original Repo Cleanup
1. Delete migrated code and tests from `claude-data-skills`.
2. Update `pyproject.toml` to remove stale entry points and dependencies.
3. Update documentation (`SKILLS.md`, `README.md`, `GEMINI.md`) to point to the new standalone tool.

## 6. Risks & Mitigations
- **Risk:** Existing users of `claude-data-skills` lose the `/define` command.
- **Mitigation:** Provide clear instructions in the original repo on how to install `graph-sieve` to restore the functionality.
- **Risk:** Broken imports in moved code (renaming from `dictionary_agent` to `graph_sieve`).
- **Mitigation:** Perform a comprehensive find-and-replace during migration and run all tests.
