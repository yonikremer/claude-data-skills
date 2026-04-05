# GEMINI.md - Full Spectrum Graph Sieve Integration

## 🧠 Domain Knowledge: GraphRAG
This project uses a **Full Spectrum Graph Sieve** to inject domain knowledge into the AI context. It moves beyond simple term lookup to a relationship-aware **Property Graph**.

For a deep dive into the architecture, see [ARCHITECTURE_GRAPH_RAG.md](./docs/ARCHITECTURE_GRAPH_RAG.md).

## 🛠️ Automated Lookup Strategy (MANDATORY)

1. **Detection**: If you encounter an unfamiliar term (e.g., an acronym like "N-RT-RIC" or a project name), **DO NOT GUESS**.
2. **Action**: Immediately run `/define <term>`.
3. **Synthesis**:
    - Incorporate the returned definition and usage examples.
    - **Graph Context**: Use the "Knowledge Graph Context" and "Executive Summary" returned by the tool to explain how this term relates to other projects (e.g., "Prism is a sub-project of Security-Suite").
4. **Tool**: If `/define` is unavailable, use `python -m src.dictionary_agent.tools lookup "<term>"`.

## 🛡️ Security & Privacy
- All knowledge extraction and validation runs on **local private models** (Ollama/vLLM).
- No internal document content is sent to external APIs.
