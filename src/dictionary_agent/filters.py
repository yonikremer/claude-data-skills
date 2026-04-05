# Global lexicon of standard tech terms that should be ignored by default
GLOBAL_LEXICON = {
    "docker", "api", "sql", "database", "git", "python", "javascript", 
    "cloud", "server", "rest", "graphql", "kubernetes", "aws", "azure",
    "gcp", "linux", "windows", "macos", "container", "microservice",
    "frontend", "backend", "fullstack", "devops", "agile", "scrum"
}

def is_domain_specific(term: str, whitelist: list = None) -> bool:
    """
    Checks if a term is domain-specific and should be extracted.
    Returns False if the term is generic/standard tech noise.
    """
    term_lower = term.lower()
    
    # Check whitelist first (exact match case-insensitive)
    if whitelist:
        whitelist_lower = {t.lower() for t in whitelist}
        if term_lower in whitelist_lower:
            return True
            
    # Check against generic lexicon
    if term_lower in GLOBAL_LEXICON:
        return False
        
    # If not in lexicon and not whitelisted, assume it is specific
    # (Gate 3 will validate its actual relevance/definition)
    return True
