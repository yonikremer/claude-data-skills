# Consolidated Dictionary Agent Architecture (v3.3.0)

## Overview
The Dictionary Agent has been refactored into a high-precision, 5-gate pipeline designed for autonomous domain knowledge extraction and validation. It consolidates multiple redundant scripts into a single, unified entry point.

## Core Components

### 1. `DictionaryAgent` (The Orchestrator)
Location: `src/dictionary_agent/agent.py`
The main class that coordinates the extraction, filtering, discovery, and validation gates.
- **Gate 1: Strategic Sieve**: Prunes files based on project status (e.g., "decommissioned").
- **Gate 2: Multi-Format Extraction**: Unified text extraction from PDF, PPTX, DOCX, and Image-based OCR.
- **Gate 3: Base-Knowledge Filter**: Drops common industry terms (SQL, Docker, etc.) unless whitelisted.
- **Gate 4: Temporal Reconciliation**: Upgrades "PENDING" definitions to "ACTIVE" and tracks document ubiquity.
- **Gate 5: Zero-Trust Validation**: Uses a "Cynical Peer Reviewer" LLM prompt to verify facts against raw context.

### 2. `Discovery & Learning`
Location: `src/dictionary_agent/discovery.py`
- Consolidates extraction and processing logic.
- Implements "Contextual Aliasing" to link Hebrew and English terms.
- Tracks "Golden Terms" (Authority Level: SEED).

### 3. `GraphKnowledgeEngine`
Location: `src/dictionary_agent/graph_engine.py`
- Builds a `networkx` Knowledge Graph of semantic triplets.
- Generates "Community Executive Reports" using LLM summarization of term clusters.

### 4. `Tools & CLI`
Location: `src/dictionary_agent/tools.py` & `src/dictionary_agent/run_scanner.py`
- `dictionary-scan`: Automated pipeline for processing directories.
- `dictionary-lookup`: Enhanced fuzzy-search tool with graph context and community summaries.

## Usage

### Scanning a Directory
```bash
dictionary-scan /path/to/docs --dict GOLDEN_TERMS.json --seed /path/to/high_authority_doc.pdf
```

### Looking Up a Term
```bash
dictionary-lookup "Prism"
```

## Prompt Engineering
The system uses three specialized LLM roles:
1. **Senior Technical Librarian**: For high-recall extraction.
2. **Cynical Peer Reviewer**: For zero-trust validation (Gate 5).
3. **Strategic Architect**: For global reasoning and community reports.
