import pytest
import os
from src.dictionary_agent.pipeline import SelectiveKnowledgePipeline
from src.dictionary_agent.models import Dictionary
from unittest.mock import patch

def test_seed_prioritization():
    # 1. Setup seed and normal docs in a unique test folder
    test_dir = "tests/data_priority"
    os.makedirs(test_dir, exist_ok=True)
    seed_file = os.path.join(test_dir, "onboarding.txt")
    normal_file = os.path.join(test_dir, "random.txt")
    
    with open(seed_file, "w") as f: f.write("Project Prism Onboarding")
    with open(normal_file, "w") as f: f.write("Project Prism Random")
    
    # 2. Setup pipeline with seed_paths
    pipeline = SelectiveKnowledgePipeline(seed_paths=[seed_file])
    
    # 3. Mock extraction
    with patch("src.dictionary_agent.pipeline.extract_with_llm") as mock_extract, \
         patch("src.dictionary_agent.pipeline.validate_with_llm") as mock_validate:
        
        mock_extract.side_effect = [
            # Seed doc extraction
            [{"term": "Prism", "definition": "High Quality Def", "anchor": "...", "entity_type": "PROJECT"}],
            # Normal doc extraction
            [{"term": "Prism", "definition": "Lower Quality Def", "anchor": "...", "entity_type": "PROJECT"}]
        ]
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        pipeline.process_directory(test_dir)
        
    # 4. Verify Prism has SEED authority
    assert pipeline.dictionary.entries["Prism"].authority_level == "SEED"
    assert pipeline.dictionary.entries["Prism"].is_golden is True

def test_pending_to_active_upgrade():
    pipeline = SelectiveKnowledgePipeline()
    os.makedirs("tests/data", exist_ok=True)
    doc1 = "tests/data/report.txt"
    doc2 = "tests/data/onboarding.txt"
    
    with open(doc1, "w") as f: f.write("Project Zephyr Revenue")
    with open(doc2, "w") as f: f.write("Project Zephyr: A high-speed network.")

    with patch("src.dictionary_agent.pipeline.extract_with_llm") as mock_extract, \
         patch("src.dictionary_agent.pipeline.validate_with_llm") as mock_validate:
        
        mock_extract.side_effect = [
            # First doc: Pending
            [{"term": "Zephyr", "definition": "[PENDING]", "anchor": "Zephyr Revenue", "entity_type": "PROJECT"}],
            # Second doc: Active
            [{"term": "Zephyr", "definition": "High-speed network", "anchor": "Project Zephyr", "entity_type": "PROJECT"}]
        ]
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        pipeline.process_document(doc1)
        assert pipeline.dictionary.entries["Zephyr"].status == "PENDING_DEFINITION"
        
        pipeline.process_document(doc2)
        assert pipeline.dictionary.entries["Zephyr"].status == "ACTIVE"
        assert pipeline.dictionary.entries["Zephyr"].definition == "High-speed network"
