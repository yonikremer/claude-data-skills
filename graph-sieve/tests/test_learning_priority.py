import pytest
import os
from graph_sieve.agent import DictionaryAgent
from graph_sieve.models import Dictionary
from unittest.mock import patch

def test_seed_prioritization():
    # 1. Setup seed and normal docs in a unique test folder
    test_dir = "tests/data_priority"
    os.makedirs(test_dir, exist_ok=True)
    seed_file = os.path.join(test_dir, "onboarding.txt")
    normal_file = os.path.join(test_dir, "random.txt")
    
    with open(seed_file, "w", encoding="utf-8") as f: f.write("Project Prism Onboarding")
    with open(normal_file, "w", encoding="utf-8") as f: f.write("Project Prism Random")
    
    # 2. Setup agent with seed_paths
    agent = DictionaryAgent(seed_paths=[seed_file])
    
    # 3. Mock extraction
    with patch("graph_sieve.agent.extract_with_llm") as mock_extract, \
         patch("graph_sieve.agent.validate_with_llm") as mock_validate:
        
        mock_extract.side_effect = [
            # Seed doc extraction
            [{"term": "Prism", "overview": "High Quality Def", "anchor": "...", "entity_type": "PROJECT"}],
            # Normal doc extraction
            [{"term": "Prism", "overview": "Lower Quality Def", "anchor": "...", "entity_type": "PROJECT"}]
        ]
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        agent.process_directory(test_dir)
        
    # 4. Verify Prism has SEED authority
    assert agent.dictionary.entries["Prism"].authority_level == "SEED"
    assert agent.dictionary.entries["Prism"].is_golden is True

def test_pending_to_active_upgrade():
    agent = DictionaryAgent()
    os.makedirs("tests/data", exist_ok=True)
    doc1 = "tests/data/report.txt"
    doc2 = "tests/data/onboarding.txt"
    
    with open(doc1, "w", encoding="utf-8") as f: f.write("Project Zephyr Revenue")
    with open(doc2, "w", encoding="utf-8") as f: f.write("Project Zephyr: A high-speed network.")

    with patch("graph_sieve.agent.extract_with_llm") as mock_extract, \
         patch("graph_sieve.agent.validate_with_llm") as mock_validate:
        
        mock_extract.side_effect = [
            # First doc: Pending
            [{"term": "Zephyr", "overview": "[PENDING]", "anchor": "Zephyr Revenue", "entity_type": "PROJECT"}],
            # Second doc: Active
            [{"term": "Zephyr", "overview": "High-speed network", "anchor": "Project Zephyr", "entity_type": "PROJECT"}]
        ]
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        agent.process_document(doc1)
        assert agent.dictionary.entries["Zephyr"].status == "PENDING_DEFINITION"
        
        agent.process_document(doc2)
        assert agent.dictionary.entries["Zephyr"].status == "ACTIVE"
        assert agent.dictionary.entries["Zephyr"].overview == "High-speed network"
