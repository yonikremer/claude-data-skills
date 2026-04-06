# Selective Knowledge Injection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a 4-gate verifiable knowledge injection pipeline to reduce noise and memory bloat.

**Architecture:** A sequential pipeline that filters generic terms, extracts facts with source anchors, and validates them via logical entailment before storing them in a layered (L1/L2) memory system.

**Tech Stack:** Python, `python-docx`, `extract-msg`, `sentence-transformers` (for L2), `pytest`.

---

### Task 1: Multi-Format Extraction (Gate 0)

**Files:**
- Modify: `src/dictionary_agent/extractor.py`
- Test: `tests/dictionary_agent/test_extractor_extended.py`

- [ ] **Step 1: Install dependencies**

Run: `pip install python-docx extract-msg`

- [ ] **Step 2: Write failing test for DOCX and MSG**

```python
import pytest
from src.dictionary_agent.extractor import extract_text_from_docx, extract_text_from_msg

def test_extract_docx():
    # Assume a dummy docx exists or create one
    text = extract_text_from_docx("tests/data/sample.docx")
    assert "project" in text.lower()

def test_extract_msg():
    text = extract_text_from_msg("tests/data/sample.msg")
    assert "subject" in text.lower()
```

- [ ] **Step 3: Implement DOCX and MSG extractors**

```python
from docx import Document
import extract_msg

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_msg(file_path):
    msg = extract_msg.Message(file_path)
    return f"Subject: {msg.subject}\nBody: {msg.body}"
```

- [ ] **Step 4: Run tests and commit**

Run: `pytest tests/dictionary_agent/test_extractor_extended.py`

---

### Task 2: Base-Knowledge Suppression (Gate 1)

**Files:**
- Create: `src/dictionary_agent/filters.py`
- Test: `tests/dictionary_agent/test_filters.py`

- [ ] **Step 1: Write failing test for Lexicon Filter**

```python
from src.dictionary_agent.filters import is_domain_specific

def test_filter_generic():
    assert is_domain_specific("Docker") is False
    assert is_domain_specific("Prism", whitelist=["Prism"]) is True
```

- [ ] **Step 2: Implement Filter with Whitelist**

```python
GLOBAL_LEXICON = {"docker", "api", "sql", "database", "git"} # Simplified for plan

def is_domain_specific(term, whitelist=None):
    if whitelist and term.lower() in [t.lower() for t in whitelist]:
        return True
    return term.lower() not in GLOBAL_LEXICON
```

- [ ] **Step 3: Run tests and commit**

---

### Task 3: Verifiable Extraction (Gate 2)

**Files:**
- Create: `src/dictionary_agent/discovery.py`
- Test: `tests/dictionary_agent/test_discovery.py`

- [ ] **Step 1: Write failing test for Anchored Extraction**

```python
from src.dictionary_agent.discovery import extract_with_anchors

def test_anchored_extraction():
    text = "The project Prism uses port 8080."
    result = extract_with_anchors(text)
    assert result[0]["term"] == "Prism"
    assert "port 8080" in result[0]["anchor"]
```

- [ ] **Step 2: Implement Extraction Logic (Mock LLM response structure)**

```python
def extract_with_anchors(text):
    # Logic to call LLM and ensure 'anchor' key is present
    return [{"term": "Prism", "definition": "Internal project", "anchor": "project Prism uses port 8080"}]
```

---

### Task 4: Hallucination Validator (Gate 3)

**Files:**
- Create: `src/dictionary_agent/validator.py`

- [ ] **Step 1: Implement Entailment Validator**

```python
def validate_definition(raw_text, definition):
    # Logic to ask LLM: 'Does raw_text logically imply definition?'
    # Return True if consistent, False otherwise.
    return True 
```

---

### Task 5: Layered Storage (L1/L2)

**Files:**
- Modify: `src/dictionary_agent/storage.py`

- [ ] **Step 1: Implement Layered Retrieval**

```python
def get_term(term, l1_cache):
    if term in l1_cache:
        return l1_cache[term]
    return fetch_from_l2(term) # Placeholder for Vector DB call
```

---

### Task 6: Orchestration Pipeline

- [ ] **Step 1: Connect all gates into a single `process_document(file_path)` function.**
- [ ] **Step 2: Run end-to-end integration test.**
