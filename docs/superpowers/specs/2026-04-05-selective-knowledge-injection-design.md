# Design Spec: Selective Knowledge Injection & Verifiable Extraction

**Date:** 2026-04-05  
**Status:** Draft  
**Topic:** Improving "Dictionary Agent" relevance and reducing memory bloat via a multi-layered filtering and verification pipeline.

## 1. Problem Statement
The current "Dictionary Agent" acts as a greedy extractor, pulling every technical term and informal fragment into the model's memory. This leads to:
1.  **Noise:** Cluttering the context with generic terms (e.g., "Docker", "API").
2.  **Memory Bloat:** Irrelevant fragments from Slack logs/emails filling the limited context window.
3.  **Hallucination Risk:** A "broken telephone" effect where AI summaries misinterpret informal internal docs without grounding.

## 2. Proposed Architecture: The "Selective Sieve"
We replace the greedy pipeline with a four-gate verifiable process.

### 2.0 Gate 0: Multi-Format Extraction
*   **Purpose:** Handle a wide variety of internal data formats beyond standard PDF/PPTX.
*   **Supported Formats:** 
    *   **Microsoft Word:** `.doc`, `.docx` (via `python-docx`).
    *   **Outlook Emails:** `.msg` (via `extract-msg`).
    *   **Text/Logs:** `.txt`, `.log`, `.md`.
*   **Fix: Unknown Format Fallback.** For unsupported or unknown binary formats, the system uses a "Generic Text Scraper" (e.g., `unstructured` library) to attempt a best-effort extraction rather than failing.

### 2.1 Gate 1: Base-Knowledge Suppression
*   **Purpose:** Prevent common industry terms from entering the project-specific dictionary.
*   **Logic:** Filter terms against a "Global Industry Lexicon" (Pre-compiled list of 5,000+ common tech terms).
*   **Fix:** **Protected Project Whitelist.** Terms like "Prism" or "Cortex" that appear in a specific "Protected Terms" list bypass this gate entirely to prevent over-filtering.

### 2.2 Gate 2: Verifiable Extraction (Grounding)
*   **Purpose:** Ensure every definition is anchored in reality.
*   **Logic:** For every term extracted from informal sources (Slack, emails), the agent **must** find a direct "Source Quote."
*   **Output:** A high-density summary paired with its original "Anchor Quote."

### 2.3 Gate 3: The Hallucination Validator
*   **Purpose:** Zero-trust verification of the summary.
*   **Logic:** A separate, low-temperature LLM cross-checks the proposed definition against the original raw text.
*   **Scoring:** Uses **Logical Entailment** (Does text A logically imply claim B?) rather than exact word matching.
*   **Outcome:** Terms with contradictions are flagged for human review; consistent terms are stored.

## 3. Storage & Layered Retrieval
To prevent memory bloat, definitions are not loaded "all at once."

1.  **L1 Cache (Active Task):** A small JSON file injected into the immediate prompt context containing terms directly related to the current task.
2.  **L2 Repository (Semantic Memory):** A structured repository (Vector DB or Knowledge Graph). Definitions are fetched **on-demand** using `/define <term>` only when detected in the user's message.
3.  **Archival Worker:** Automatically moves unused terms (30+ days idle) to a secondary "Archive" to keep L2 lean.

## 4. Mitigations & Resilience
*   **Recency Weighting:** If a 2026 README conflicts with a 2024 Slack log, the system automatically prioritizes the 2026 source.
*   **Recursive Extraction (Gate 0):** Handles attachments inside `.msg` or `.docx` files by unpacking them and re-routing them through the pipeline.
*   **OCR Fallback:** Detects "Image-Only" documents and triggers an OCR pass to prevent missing "Hidden Knowledge."
*   **Lazy-Loading Plugins:** Prevents system crashes if specialized libraries (like `extract-msg`) are missing; provides graceful degradation.
*   **Cross-Source Reconciliation:** Merges partial definitions found in different formats (e.g., a `.docx` definition enriched by a Slack `.log` example) instead of creating duplicates.
*   **Batch Processing:** To maintain performance, the system processes document "chunks" in parallel rather than sentence-by-sentence.
*   **Human-in-the-Loop:** High-confidence terms are auto-saved; low-confidence terms (soft-match failures) are sent to a `NEEDS_REVIEW.md` file.

## 5. Success Criteria
*   **Relevance:** 90%+ reduction in generic "Industry Noise" (e.g., no more definitions for "SQL").
*   **Grounding:** Zero "un-anchored" definitions added from informal sources.
*   **Context Efficiency:** Model memory remains focused on the specific project domain, not the entire internal doc repository.
