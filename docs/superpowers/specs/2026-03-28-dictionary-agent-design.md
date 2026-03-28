# Design Specification: AI-Ready Dictionary Agent (Option 1 - Live Tool)

## 1. Overview
The **AI-Ready Dictionary Agent** is a system designed to bridge the gap between AI understanding and domain-specific technical queries. It proactively extracts terms and definitions from a network drive (PDF, PPTX, Confluence-PDFs), stores them in a structured JSON dictionary, and provides a real-time lookup tool for other AI agents to use during task execution.

## 2. Architecture

### 2.1 Core Components
*   **Source Folder (Windows NFS)**: A directory containing `.pdf`, `.pptx`, and exported Confluence PDFs.
*   **Extractor Agent (The "Builder")**: A Python-based agent that scans the source folder, extracts raw text, and uses an LLM to identify technical terms and context-aware definitions.
*   **Dictionary Storage (`dictionary.json`)**: A structured JSON database of all terms, definitions, source references, and context-specific usage examples.
*   **Golden Dictionary (`GOLDEN_TERMS.md`)**: A "Top 20" list of terms that are injected directly into the AI's system context via `GEMINI.md`.
*   **`lookup_term` Tool**: A custom MCP tool that allows the AI to query the `dictionary.json` in real-time when it encounters an unknown term.

### 2.2 Extraction & Discovery Process
1.  **File Discovery**: The Extractor Agent identifies new or modified files in the source folder.
2.  **Text Extraction**: 
    *   **PDF/Confluence-PDF**: Uses `pdfplumber` for text and layout extraction.
    *   **PPTX**: Uses `python-pptx` to extract slide content and speaker notes.
3.  **AI-Powered Term Discovery**:
    *   **Step 1: Chunking**: The extracted text is divided into manageable chunks.
    *   **Step 2: LLM Pass**: The LLM analyzes each chunk to find "new" technical terms, project names, and acronyms.
    *   **Step 3: Iterative Learning**: The AI compares the found terms against the *partially populated* `dictionary.json`.
        *   **If Term Exists**: The AI evaluates if the new context adds a different meaning or usage. If so, it appends a "New Usage Example" or "Refined Definition" to the existing entry.
        *   **If Term is New**: A new entry is created with a concise, AI-ready definition.
4.  **Enrichment**: The AI identifies relationships between terms (e.g., "Term A is a component of Term B") and adds these links to the JSON.

### 2.3 AI Integration (The "Lookup" Step)
*   **Golden Terms**: The Top 20 terms are always present in the AI's memory.
*   **`lookup_term(term="XYZ")`**: 
    1.  AI encounters a term not in its context.
    2.  AI calls the `lookup_term` tool.
    3.  The tool searches `dictionary.json` (exact match + fuzzy match).
    4.  The tool returns the `definition`, `source_file`, and `usage_context`.

## 3. Data Flow
`[Source File]` -> `[Text Extraction]` -> `[AI Term Discovery (w/ Prior Knowledge)]` -> `[dictionary.json Update]` -> `[AI Tool Execution]`

## 4. Error Handling & Edge Cases
*   **Conflict Resolution**: When multiple definitions for the same term are found across different sources, both are stored as "Alternative Contexts."
*   **Corrupt Files**: Files that fail extraction are logged and skipped to prevent system freezes.
*   **Missing Terms**: If the `lookup_term` tool fails to find a term, it returns a "Term Not Found" message, and the AI is instructed to ask the user for clarification.

## 5. Success Criteria
*   **Accuracy**: Extracted definitions must be concise and technically correct for an AI agent.
*   **Efficiency**: The `lookup_term` tool must respond in < 500ms.
*   **Iterative Growth**: The dictionary must automatically reflect updates to the source documents without manual intervention.

## 6. Testing Strategy
1.  **Extraction Test**: Run the Extractor on a "Mock PDF" containing 5 unique technical terms and verify they appear in `dictionary.json`.
2.  **Learning Test**: Run the Extractor on a "Mock PPTX" that uses an *existing* term in a new context and verify the dictionary entry is enriched, not duplicated.
3.  **Tool Test**: Execute a query where the AI must define an "unknown" term and verify it correctly calls `lookup_term`.
