import pytest
import os
from unittest.mock import patch
from graph_sieve.agent import DictionaryAgent
from graph_sieve.models import Dictionary

@pytest.fixture
def mock_llm_discovery():
    with patch("graph_sieve.agent.extract_with_llm") as mock:
        yield mock

@pytest.fixture
def mock_llm_validator():
    with patch("graph_sieve.agent.validate_with_llm") as mock:
        yield mock

def test_pipeline_full_run(mock_llm_discovery, mock_llm_validator):
    # Configure mocks
    mock_llm_discovery.return_value = [
        {"term": "Prism", "definition": "Secure communication project", "anchor": "Project Prism uses port 8080"}
    ]
    mock_llm_validator.return_value = {"is_valid": True}

    # Create a temporary text file with a new term
    test_file = "tests/data/test_doc.txt"
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Project Prism uses port 8080 for secure communication. It is superior to project Docker.")
        
    pipeline = DictionaryAgent()
    added = pipeline.process_document(test_file)
    
    # 'Prism' should be added
    assert "Prism" in added
    
    # Check dictionary state
    assert "Prism" in pipeline.dictionary.entries
    
def test_pipeline_whitelist(mock_llm_discovery, mock_llm_validator):
    mock_llm_discovery.return_value = [
        {"term": "SQL", "definition": "Database system", "anchor": "Project SQL is a new database system"}
    ]
    mock_llm_validator.return_value = {"is_valid": True}

    test_file = "tests/data/test_whitelist.txt"
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Project SQL is a new database system.")
        
    # SQL is generic, but we whitelist it
    pipeline = DictionaryAgent(whitelist=["SQL"])
    added = pipeline.process_document(test_file)
    
    assert "SQL" in added
    assert "SQL" in pipeline.dictionary.entries
