from typing import List, Dict
import re

def extract_with_anchors(text: str) -> List[Dict]:
    """
    Extracts technical terms from text and provides a direct source anchor for each.
    In a production system, this would use an LLM with a prompt that mandates anchors.
    """
    # Rule-based discovery for testing/mocking
    # Looks for 'project <Name>' as a pattern
    results = []
    
    # Simple regex to find "project [CapitalizedWord]"
    project_matches = re.finditer(r"project\s+([A-Z][a-zA-Z0-9_-]*)", text, re.IGNORECASE)
    
    for match in project_matches:
        term = match.group(1)
        start_idx = match.start()
        
        # Get surrounding context as an 'anchor' (approx 100 chars around)
        window = 100
        anchor_start = max(0, start_idx - window)
        anchor_end = min(len(text), start_idx + window)
        anchor = text[anchor_start:anchor_end].strip()
        
        results.append({
            "term": term,
            "definition": f"A project named {term}.",
            "anchor": anchor,
            "is_new": True
        })
        
    return results
