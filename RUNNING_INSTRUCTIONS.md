# Running Instructions: Full Spectrum GraphRAG Sieve

This guide provides step-by-step instructions for running the GraphRAG pipeline on your internal documentation.

## 1. Prerequisites

### Local Model Setup (Private & Secure)
The system is designed to run on your local hardware. We recommend using **Ollama**.

1.  **Install Ollama**: [ollama.com](https://ollama.com)
2.  **Pull the Model**:
    ```bash
    ollama pull llama3
    ```
3.  **Ensure Ollama is Running**: The pipeline connects to `http://localhost:11434`.

### Python Environment
1.  **Install Dependencies**:
    ```bash
    pip install -e .
    pip install llama-index llama-index-llms-ollama pyOneNote extract-msg python-docx networkx requests
    ```

---

## 2. Configuration

Create a configuration script (e.g., `run_ingestion.py`) to define your organizational focus and decommissioned domains.

```python
from src.dictionary_agent.pipeline import SelectiveKnowledgePipeline
from src.dictionary_agent.strategic_filter import StrategicSieve
from src.dictionary_agent.storage import load_dictionary, save_dictionary

# 1. Setup Strategic Sieve (Gate 1)
# Add keywords for abandoned projects or domains here
sieve = StrategicSieve(
    decommissioned_keywords=["Project-Zephyr", "Legacy-Portal", "Sales-2017"]
)

# 2. Define Seed Documents (High Authority)
# Onboarding docs, workplans, and team presentations go here
seeds = [
    "./docs/onboarding",
    "./docs/branch_workplans/2026_strategy.pdf"
]

# 3. Initialize Pipeline
pipeline = SelectiveKnowledgePipeline(
    seed_paths=seeds,
    strategic_sieve=sieve
)

# 4. Run Ingestion on Full Repository
pipeline.process_directory("./network_file_system")

# 5. Generate Community Reports (Global Reasoning)
pipeline.graph_engine.generate_community_reports()

# 6. Save Knowledge Graph
save_dictionary(pipeline.dictionary, "storage/knowledge_graph.json")
```

---

## 3. Running the Pipeline

### Development / Offline Mode (No Tokens)
To test the pipeline without calling the LLM, use the built-in mock mode:
```powershell
$env:MOCK_LLM="true"
python run_ingestion.py
```

### Production Mode (Local LLM)
Ensure Ollama is running and execute:
```bash
python run_ingestion.py
```

---

## 4. Querying the Knowledge Graph

Once the graph is built, you can use the built-in lookup tools to get context-aware definitions.

### Using the CLI Tool
```bash
python -m src.dictionary_agent.tools lookup "Project Prism"
```

### Understanding the Output
The tool returns:
1.  **Definition**: The verified "Golden" definition.
2.  **Ubiquity**: How many unique documents this term appeared in.
3.  **Graph Context**: Relationships (e.g., "Prism is a sub-project of Security-Suite").
4.  **Executive Summary**: A high-level report of the thematic cluster the term belongs to.

---

## 5. Maintenance & Scaling

*   **Change Detection**: The system uses SHA-256 hashing. It will only process documents that have been modified since the last run.
*   **Temporal Cleanup**: Terms not seen in documents for 3+ years are automatically flagged as `[DORMANT]`.
*   **Manual Review**: Any extraction that fails the **Gate 5 (Zero-Trust Validator)** is logged but not added to the Golden Dictionary. Review your logs periodically to tune the validator strictness.
