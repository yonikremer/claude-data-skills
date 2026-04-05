import pytest
import os
from src.dictionary_agent.pipeline import SelectiveKnowledgePipeline
from src.dictionary_agent.models import Dictionary
from unittest.mock import patch, MagicMock

def test_full_workflow_end_to_end():
    # 1. Setup mock data
    test_files = {
        "tests/data/readme.md": "Project Prism is a new security suite.",
        "tests/data/notes.txt": "Prism depends on project Cortex for identity."
    }
    
    for path, content in test_files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
    # 2. Setup Pipeline
    pipeline = SelectiveKnowledgePipeline()
    
    # 3. Process files with MOCK_LLM enabled (should be in env)
    # Mocking extraction to return relationships for notes.txt
    with patch("src.dictionary_agent.pipeline.extract_with_llm") as mock_extract, \
         patch("src.dictionary_agent.pipeline.validate_with_llm") as mock_validate:
        
        # readme.md extraction
        mock_extract.side_effect = [
            [{"term": "Prism", "definition": "A security suite.", "anchor": "Project Prism", "entity_type": "PROJECT"}],
            [{
                "term": "Prism", 
                "definition": "...", 
                "anchor": "Prism depends on project Cortex", 
                "entity_type": "PROJECT",
                "relationships": [{"target": "Cortex", "type": "DEPENDS_ON"}]
            }]
        ]
        
        # validation
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        pipeline.process_document("tests/data/readme.md")
        pipeline.process_document("tests/data/notes.txt")
        
    # 4. Verify results
    assert "Prism" in pipeline.dictionary.entries
    assert len(pipeline.dictionary.relationships) == 1
    rel = pipeline.dictionary.relationships[0]
    assert rel.subject == "Prism"
    assert rel.relationship == "DEPENDS_ON"
    assert rel.object == "Cortex"
    
    # 5. Verify graph walk
    context = pipeline.graph_engine.get_context_map("Prism")
    assert "DEPENDS_ON" in context
    assert "Cortex" in context
