# Graph-Sieve 🕸️📊

**Full Spectrum Graph Sieve - Automated Technical Term Extraction and Relationship Mapping**

`graph-sieve` is a standalone utility and service designed to extract relationship-aware domain knowledge from internal documents (.docx, .pptx, .msg, .pdf). It uses a multi-gate verifiable pipeline with local models (Ollama/vLLM) to build a structured knowledge graph of technical terms and their relationships.

## Features

- **Multi-Format Extraction**: Supports PDF, PPTX, DOCX, MSG, and images (via OCR).
- **OCR Integration**: Built-in OCR support using `easyocr` for processing scanned documents and images.
- **Graph-Based Knowledge**: Moves beyond simple term lookup to a relationship-aware Property Graph.
- **Local-First**: Designed to run with local private models to ensure security and privacy.
- **MCP Server**: Integrated Model Context Protocol (MCP) server for easy integration with AI agents like Claude or Gemini.

## Installation

```bash
pip install .
```

## Usage

### CLI Commands

The package provides several CLI entry points:

- `graph-sieve-scan`: Scan a directory or file for technical terms.
- `graph-sieve-lookup`: Lookup a term in the extracted knowledge base.
- `graph-sieve-visualize`: Visualize the knowledge graph.
- `graph-sieve-mcp`: Run the MCP server.
- `graph-sieve-whois`: Identify the source of a term.

### Example: Scanning a Directory

```bash
graph-sieve-scan --dir ./my-docs --output ./knowledge-base.json
```

### Example: Looking up a Term

```bash
graph-sieve-lookup "N-RT-RIC"
```

## AI Agent Integration

### Gemini CLI

Add the following command to your `.gemini/commands/define.toml`:

```toml
description = "Lookup a technical term in the dictionary"
prompt = """
Use the `lookup_term` tool from `graph_sieve.tools` to find the definition and context for: {{args}}.
If found, explain how it relates to the current task. If not found, check the Golden Terms or ask for clarification.
"""
```

Update your `GEMINI.md` to reference `graph-sieve-lookup` as a fallback tool.

## License

MIT License. See [LICENSE](LICENSE) for details.
