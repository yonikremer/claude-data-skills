# Architecture: Full Spectrum Graph Sieve (GraphRAG)

This document describes the agentic workflow for selective knowledge injection and relationship-aware reasoning using private local models.

## 1. Overview
The **Full Spectrum Graph Sieve** is a production-grade knowledge ingestion system designed to solve the "Broken Telephone" effect in standard RAG. Instead of simple vector retrieval, it builds a **Semantic Property Graph** grounded in verbatim source anchors.

## 2. The 5-Gate Verifiable Pipeline
To ensure high accuracy and low token usage, every document passes through five distinct "Gates":

### Gate 1: Strategic Sieve (Negative Whitelist)
Filters out decommissioned projects and abandoned domains at the file path level. This prevents the pipeline from processing "Zombie" data (e.g., projects that were closed years ago).

### Gate 2: Multi-Format Extraction
Handles a wide variety of internal data formats using specialized parsers (.docx, .msg, .one, .pdf, .txt).

### Gate 3: Base-Knowledge Suppression
Uses a deterministic "Global Industry Lexicon" to filter out standard tech noise (e.g., "SQL", "API", "Docker").

### Gate 4: Verifiable Extraction (Anchoring)
A "Technical Librarian" agent extracts Semantic Triplets with verbatim grounding quotes.

### Gate 5: Zero-Trust Validator (Hallucination Check)
A cynical "Peer Reviewer" agent cross-checks every extraction against the raw context using logical entailment.

## 3. Advanced Learning & Prioritization

### Seed Document Prioritization
High-authority documents (Onboarding docs, Team Presentations, Workplans) can be designated as **Seed Paths**.
- **Truth Layer:** Seed documents are processed first to establish the foundational truth.
- **Authority Marking:** Terms extracted from seeds are marked as `authority_level="SEED"` and `is_golden=True`.

### Incremental Learning (Pending Definitions)
The system handles the "Cold Start" problem where a term is seen (e.g., in a list) but lacks a definition.
- **Pending State:** Terms without clear definitions are stored as `PENDING_DEFINITION`.
- **Auto-Upgrade:** If a later document (especially a Seed doc) provides a high-quality definition, the entry is automatically upgraded to `ACTIVE`.
- **Knowledge Preservation:** Ensures that important project names are tracked even before their purpose is fully documented.

## 4. Scaling for 10 Years of Data
The system includes advanced features to handle thousands of documents and a decade of institutional memory:

### Temporal Reconciliation
- **Reverse-Chronological Indexing:** Newest documents set the "Truth Layer."
- **Status Tracking:** Nodes automatically transition between `ACTIVE`, `LEGACY`, and `DORMANT` based on recency and appearance frequency.

### SHA-256 Hashing
- Prevents redundant LLM calls by hashing every file. If a file hasn't changed, the pipeline skips it, saving 90%+ of token costs on repeat runs.

### Community Summarization (Leiden Pattern)
- Groups thousands of nodes into thematic "Communities" (e.g., "The Security Infrastructure Cluster").
- Generates **Executive Summary Reports** for each cluster, allowing the AI to reason globally without hitting context limits.

## 4. Private Model Integration
- **Private Hardware:** Designed to run on local hardware via **Ollama** or **vLLM**.
- **Data Sovereignty:** Your private organizational data never leaves your infrastructure.
- **Mock Mode:** Built-in `$env:MOCK_LLM="true"` mode for offline testing and development.

## 5. Usage
To index a directory:
```python
from src.dictionary_agent.pipeline import SelectiveKnowledgePipeline
pipeline = SelectiveKnowledgePipeline()
pipeline.process_directory("./my_internal_docs")
```

To lookup a term with graph context:
```python
from src.dictionary_agent.graph_engine import GraphKnowledgeEngine
engine = GraphKnowledgeEngine(my_dictionary)
context = engine.get_context_map("Project Prism")
print(context)
```
