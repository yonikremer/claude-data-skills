from typing import List

# Industry common terms that are usually noise unless they have an internal meaning
COMMON_REJECTS = {
    "SQL", "API", "DOCKER", "KUBERNETES", "AWS", "PYTHON", "GIT", "REST", "JSON", 
    "DATABASE", "SERVER", "CLOUD", "FRONTEND", "BACKEND", "SECURITY", "LINUX"
}

def is_domain_specific(term: str, whitelist: List[str] = None) -> bool:
    """
    Pitfall 5 Fix: Contrastive Filtering.
    Checks if a term is specific enough to the organization.
    """
    if not term or len(term) < 2:
        return False
        
    term_upper = term.upper()
    whitelist = [w.upper() for w in whitelist] if whitelist else []
    
    # 1. Whitelist always passes
    if term_upper in whitelist:
        return True
        
    # 2. Reject common industry terms unless they are whitelisted
    # Note: The extraction prompt also handles this by accepting 'The API' (specific)
    # but rejecting 'API' (generic). This code handles the final safety gate.
    if term_upper in COMMON_REJECTS:
        return False
        
    # 3. Reject generic single common words (heuristic)
    if term_upper in {"PROJECT", "SYSTEM", "DOCUMENT", "TEAM", "MANAGER", "MEETING"}:
        return False
        
    return True
