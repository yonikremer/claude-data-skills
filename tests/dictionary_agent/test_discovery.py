from src.dictionary_agent.discovery import extract_with_anchors

def test_anchored_extraction():
    # Sample text with a clear term and context
    text = "The project Prism uses port 8080 for secure communication."
    
    # In a real system, this would call an LLM. 
    # For now, we test the interface and a mockable extraction logic.
    result = extract_with_anchors(text)
    
    assert len(result) > 0
    assert "term" in result[0]
    assert "definition" in result[0]
    assert "anchor" in result[0]
    
    # Check that Prism was extracted with its context anchor
    prism_entry = next((item for item in result if item["term"] == "Prism"), None)
    assert prism_entry is not None
    assert "port 8080" in prism_entry["anchor"]
    assert "secure communication" in prism_entry["anchor"]
