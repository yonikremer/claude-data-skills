def validate_definition(raw_text: str, definition: str) -> bool:
    """
    Validates that a definition is logically consistent with the source text.
    In a production system, this would use a low-temperature LLM call.
    """
    # Simple rule-based mock: check if major keywords in definition 
    # (longer than 4 chars) are present in the raw_text.
    
    # Ignore common words
    ignore = {"project", "internal", "named", "with", "this", "that"}
    
    def_words = set(definition.lower().replace(".", "").split())
    raw_words = set(raw_text.lower().replace(".", "").split())
    
    # Significant words in definition
    sig_def_words = {w for w in def_words if len(w) > 4 and w not in ignore}
    
    if not sig_def_words:
        return True # Can't disprove if no significant words
        
    # Check if any significant word in definition is NOT in raw_text
    # (Mocking 'hallucination' if a new entity like 'coffee' appears)
    for word in sig_def_words:
        if word not in raw_words:
            # Check for partial matches (e.g. 'firewall' in 'firewalls')
            if not any(word in rw for rw in raw_words):
                return False
                
    return True
