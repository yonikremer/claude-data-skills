import pytest
import os
from graph_sieve.agent import DictionaryAgent
from graph_sieve.models import Dictionary
from unittest.mock import patch

def test_document_counter_increment():
    # 1. Setup mock data
    os.makedirs("tests/data", exist_ok=True)
    doc1_path = "tests/data/doc1.txt"
    doc2_path = "tests/data/doc2.txt"
    with open(doc1_path, "w", encoding="utf-8") as f:
        f.write("Project Prism is mentioned multiple times in Prism doc.")
    with open(doc2_path, "w", encoding="utf-8") as f:
        f.write("Another mention of Project Prism.")
        
    agent = DictionaryAgent()
    
    # 2. Mock LLM to return Prism multiple times for doc1, and once for doc2
    with patch("graph_sieve.agent.extract_with_llm") as mock_extract, \
         patch("graph_sieve.agent.validate_with_llm") as mock_validate:
        
        mock_extract.side_effect = [
            # doc1: Prism mentioned twice
            [
                {"term": "Prism", "overview": "...", "anchor": "Prism 1"},
                {"term": "Prism", "overview": "...", "anchor": "Prism 2"}
            ],
            # doc2: Prism mentioned once
            [
                {"term": "Prism", "overview": "...", "anchor": "Prism 3"}
            ]
        ]
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        agent.process_document(doc1_path)
        # After doc1, count should be 1
        assert agent.dictionary.entries["Prism"].document_count == 1
        
        agent.process_document(doc2_path)
        # After doc2, count should be 2
        assert agent.dictionary.entries["Prism"].document_count == 2
