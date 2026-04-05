import pytest
import os
from src.dictionary_agent.pipeline import SelectiveKnowledgePipeline
from src.dictionary_agent.models import Dictionary
from unittest.mock import patch

def test_document_counter_increment():
    # 1. Setup mock data
    os.makedirs("tests/data", exist_ok=True)
    with open("tests/data/doc1.txt", "w", encoding="utf-8") as f:
        f.write("Project Prism is mentioned multiple times in Prism doc.")
    with open("tests/data/doc2.txt", "w", encoding="utf-8") as f:
        f.write("Another mention of Project Prism.")
        
    pipeline = SelectiveKnowledgePipeline()
    
    # 2. Mock LLM to return Prism multiple times for doc1, and once for doc2
    with patch("src.dictionary_agent.pipeline.extract_with_llm") as mock_extract, \
         patch("src.dictionary_agent.pipeline.validate_with_llm") as mock_validate:
        
        mock_extract.side_effect = [
            # doc1: Prism mentioned twice
            [
                {"term": "Prism", "definition": "...", "anchor": "Prism 1"},
                {"term": "Prism", "definition": "...", "anchor": "Prism 2"}
            ],
            # doc2: Prism mentioned once
            [
                {"term": "Prism", "definition": "...", "anchor": "Prism 3"}
            ]
        ]
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        pipeline.process_document("tests/data/doc1.txt")
        # After doc1, count should be 1
        assert pipeline.dictionary.entries["Prism"].document_count == 1
        
        pipeline.process_document("tests/data/doc2.txt")
        # After doc2, count should be 2
        assert pipeline.dictionary.entries["Prism"].document_count == 2
