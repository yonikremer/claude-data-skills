import pytest
import os
from graph_sieve.agent import DictionaryAgent
from graph_sieve.models import Dictionary
from unittest.mock import patch, MagicMock

def test_full_workflow_end_to_end():
    # 1. Setup mock data
    os.makedirs("tests/data", exist_ok=True)
    test_files = {
        "tests/data/readme.md": "Project Prism is a new security suite.",
        "tests/data/notes.txt": "Prism depends on project Cortex for identity."
    }
    
    for path, content in test_files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
    # 2. Setup Agent
    agent = DictionaryAgent()
    
    # 3. Process files
    with patch("graph_sieve.agent.extract_with_llm") as mock_extract, \
         patch("graph_sieve.agent.validate_with_llm") as mock_validate:
        
        # readme.md extraction
        mock_extract.side_effect = [
            [{"term": "Prism", "overview": "A security suite.", "anchor": "Project Prism", "entity_type": "PROJECT"}],
            [{
                "term": "Prism", 
                "overview": "...", 
                "anchor": "Prism depends on project Cortex", 
                "entity_type": "PROJECT",
                "relationships": [{"target": "Cortex", "type": "DEPENDS_ON"}]
            }]
        ]
        
        # validation
        mock_validate.return_value = {"is_valid": True, "status": "PASS"}
        
        agent.process_document("tests/data/readme.md")
        agent.process_document("tests/data/notes.txt")
        
    # 4. Verify results
    assert "Prism" in agent.dictionary.entries
    assert len(agent.dictionary.relationships) == 1
    rel = agent.dictionary.relationships[0]
    assert rel.subject == "Prism"
    assert rel.relationship == "DEPENDS_ON"
    assert rel.object == "Cortex"
    
    # 5. Verify graph walk
    context = agent.graph_engine.get_context_map("Prism")
    assert "DEPENDS_ON" in context
    assert "Cortex" in context
