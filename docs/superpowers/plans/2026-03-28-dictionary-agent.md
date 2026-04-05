# AI-Ready Dictionary Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:
> executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an automated dictionary agent that extracts terms from PDF/PPTX, learns iteratively, and provides a
real-time lookup tool.

**Architecture:**

1. **Storage Layer**: `dictionary.json` for all terms and `GOLDEN_TERMS.md` for Top 20.
2. **Extractor Agent**: Python script using `pdfplumber` and `python-pptx` with LLM-based term discovery and iterative
   refinement.
3. **Lookup Tool**: A custom tool interface for AI agents to query the JSON dictionary.

**Tech Stack:** Python, `pdfplumber`, `python-pptx`, `pydantic`, `pytest`.

---

### Task 1: Dictionary Storage & Schema

**Files:**

- Create: `src/dictionary_agent/models.py`
- Create: `src/dictionary_agent/storage.py`
- Test: `tests/dictionary_agent/test_storage.py`

- [ ] **Step 1: Define Dictionary Models**

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class UsageExample(BaseModel):
    context: str
    source: str
    date_added: str

class DictionaryEntry(BaseModel):
    term: str
    definition: str
    source_file: str
    usage_examples: List[UsageExample] = []
    related_terms: List[str] = []
    is_golden: bool = False

class Dictionary(BaseModel):
    entries: Dict[str, DictionaryEntry] = {}
```

- [ ] **Step 2: Implement Storage Logic**
  Implement `load_dictionary` and `save_dictionary` using JSON.

- [ ] **Step 3: Write Storage Tests**
  Verify that adding a term and saving/loading works.

- [ ] **Step 4: Commit**
  `git add src/dictionary_agent/ tests/dictionary_agent/ && git commit -m "feat: add dictionary storage and models"`

---

### Task 2: PDF & PPTX Text Extraction

**Files:**

- Create: `src/dictionary_agent/extractor.py`
- Test: `tests/dictionary_agent/test_extractor.py`

- [ ] **Step 1: Implement PDF Extraction**
  Use `pdfplumber` to extract text from a file path.

- [ ] **Step 2: Implement PPTX Extraction**
  Use `python-pptx` to extract text from slides and notes.

- [ ] **Step 3: Write Extraction Tests**
  Use mock files or small samples to verify text is retrieved.

- [ ] **Step 4: Commit**
  `git add src/dictionary_agent/extractor.py tests/dictionary_agent/test_extractor.py && git commit -m "feat: implement PDF and PPTX extraction"`

---

### Task 3: AI-Powered Term Discovery & Iterative Learning

**Files:**

- Create: `src/dictionary_agent/ai_discovery.py`
- Modify: `src/dictionary_agent/agent.py`
- Test: `tests/dictionary_agent/test_learning.py`

- [ ] **Step 1: Implement AI Term Extraction Prompt**
  Create a function that sends text chunks to the LLM with the instruction to find terms.

- [ ] **Step 2: Implement Iterative Refinement Logic**
  Logic: Before calling LLM, provide existing terms from `dictionary.json` as context.
  Instruction: "Enrich existing terms or extract new ones."

- [ ] **Step 3: Write Learning Tests**
  Verify that a term found in a second document is added as a `UsageExample` instead of a new entry.

- [ ] **Step 4: Commit**
  `git add src/dictionary_agent/ && git commit -m "feat: implement AI discovery and iterative learning"`

---

### Task 4: The `lookup_term` Tool

**Files:**

- Create: `src/dictionary_agent/tools.py`
- Modify: `.gemini/commands/lookup.toml` (or equivalent config)

- [ ] **Step 1: Implement Search Logic**
  Implement exact and fuzzy matching against `dictionary.json`.

- [ ] **Step 2: Create Tool Wrapper**
  Expose `lookup_term(term: str)` returning a formatted string for the AI.

- [ ] **Step 3: Verify Tool Execution**
  Manually test the lookup with a known term.

- [ ] **Step 4: Commit**
  `git add src/dictionary_agent/tools.py && git commit -m "feat: add lookup_term tool"`

---

### Task 5: Golden Terms & Integration

**Files:**

- Create: `GOLDEN_TERMS.md`
- Modify: `GEMINI.md`

- [ ] **Step 1: Identify Top 20 Terms**
  Run a script to find the most frequent terms in the dictionary.

- [ ] **Step 2: Generate GOLDEN_TERMS.md**
  Format them as a clean Markdown table.

- [ ] **Step 3: Update System Context**
  Add a reference to `GOLDEN_TERMS.md` in the project root's `GEMINI.md`.

- [ ] **Step 4: Commit**
  `git add GOLDEN_TERMS.md GEMINI.md && git commit -m "docs: finalize golden terms and system integration"`
