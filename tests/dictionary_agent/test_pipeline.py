import pytest
import os
from src.dictionary_agent.pipeline import SelectiveKnowledgePipeline
from src.dictionary_agent.models import Dictionary

def test_pipeline_full_run():
    # Create a temporary text file with a new term
    test_file = "tests/data/test_doc.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Project Prism uses port 8080 for secure communication. It is superior to project Docker.")
        
    pipeline = SelectiveKnowledgePipeline()
    added = pipeline.process_document(test_file)
    
    # 'Prism' should be added
    assert "Prism" in added
    # 'Docker' should be filtered out by Gate 1
    assert "Docker" not in added
    
    # Check dictionary state
    assert "Prism" in pipeline.dictionary.entries
    assert "Docker" not in pipeline.dictionary.entries
    
def test_pipeline_whitelist():
    test_file = "tests/data/test_whitelist.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Project SQL is a new database system.")
        
    # SQL is generic (Gate 1), but we whitelist it
    pipeline = SelectiveKnowledgePipeline(whitelist=["SQL"])
    added = pipeline.process_document(test_file)
    
    assert "SQL" in added
    assert "SQL" in pipeline.dictionary.entries
