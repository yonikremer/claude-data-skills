# Dictionary Agent Advanced Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement four major enhancements to the Dictionary Agent: Dynamic Prompt Injection, Interactive Visualization, Temporal Truth Layering, and an Expert Finder Tool.

**Architecture:** 
1. **Dynamic Prompts:** Update `discovery.py` to use `RELATION_TYPES` from `models.py`.
2. **Visualization:** Add `pyvis` based HTML export to `graph_engine.py` and a new `visualize.py` tool.
3. **Temporal Truth Layering:** Update `agent.py` to handle `SUPERSEDES` relationships by marking old data as `DORMANT`.
4. **Expert Finder:** Create `whois.py` to map technical experts and managers from the graph.

**Tech Stack:** Python, NetworkX, Pyvis, Pydantic, Model Context Protocol (MCP).

---

### Task 1: Dynamic Prompt Injection

**Files:**
- Modify: `src/dictionary_agent/discovery.py`

- [ ] **Step 1: Import RELATION_TYPES and update prompt**
Update `EXTRACTOR_SYSTEM_PROMPT` to be a function or dynamically generated to include the actual `RELATION_TYPES` from `models.py`.

```python
from .models import RELATION_TYPES

def get_system_prompt():
    allowed_rels = ", ".join(RELATION_TYPES.__args__) # For Literal
    return f"""...
   - Allowed Relationships: {allowed_rels}.
..."""
```

- [ ] **Step 2: Update `extract_with_llm` to use dynamic prompt**
Call `get_system_prompt()` inside `extract_with_llm`.

- [ ] **Step 3: Commit**
```bash
git add src/dictionary_agent/discovery.py
git commit -m "feat: implement dynamic prompt injection for relationship types"
```

### Task 2: Interactive Graph Visualization

**Files:**
- Modify: `src/dictionary_agent/graph_engine.py`
- Create: `src/dictionary_agent/visualize.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Install pyvis**
Run: `pip install pyvis`

- [ ] **Step 2: Add visualization method to `GraphKnowledgeEngine`**
```python
    def visualize_graph(self, output_path: str = "graph.html"):
        from pyvis.network import Network
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        # Add nodes and edges from self.dictionary.relationships
        # ...
        net.save_graph(output_path)
```

- [ ] **Step 3: Create `visualize.py` tool**
Create a script that loads the dictionary and calls `visualize_graph`.

- [ ] **Step 4: Add `dictionary-visualize` entry point to `pyproject.toml`**

- [ ] **Step 5: Commit**
```bash
git add src/dictionary_agent/graph_engine.py src/dictionary_agent/visualize.py pyproject.toml
git commit -m "feat: add interactive graph visualization tool"
```

### Task 3: Temporal Truth Layering (Conflict Resolution)

**Files:**
- Modify: `src/dictionary_agent/agent.py`
- Modify: `src/dictionary_agent/models.py`

- [ ] **Step 1: Update `DictionaryAgent.process_document`**
Identify `SUPERSEDES` relationships during extraction. If `A SUPERSEDES B`, find existing relationships involving `B` and mark them as `DORMANT`.

- [ ] **Step 2: Implement `reconcile_supersedes` method**
```python
    def reconcile_supersedes(self, subject: str, target: str):
        # Mark target as LEGACY or DORMANT
        if target in self.dictionary.entries:
            self.dictionary.entries[target].status = "LEGACY"
```

- [ ] **Step 3: Commit**
```bash
git add src/dictionary_agent/agent.py src/dictionary_agent/models.py
git commit -m "feat: implement temporal truth layering for SUPERSEDES relationships"
```

### Task 4: Expert Finder Tool (/whois)

**Files:**
- Create: `src/dictionary_agent/whois.py`
- Modify: `pyproject.toml`
- Modify: `src/dictionary_agent/mcp_server.py`

- [ ] **Step 1: Implement `whois` logic**
Search for `IS_EXPERT_OF`, `IS_MANAGER_OF`, and `REPORTS_TO` relationships to identify key people for a given term.

- [ ] **Step 2: Create `whois.py` CLI tool**

- [ ] **Step 3: Add `whois` tool to MCP server**
Expose a `whois(term)` tool in `mcp_server.py`.

- [ ] **Step 4: Add `dictionary-whois` entry point to `pyproject.toml`**

- [ ] **Step 5: Commit**
```bash
git add src/dictionary_agent/whois.py pyproject.toml src/dictionary_agent/mcp_server.py
git commit -m "feat: add expert finder whois tool and MCP integration"
```
