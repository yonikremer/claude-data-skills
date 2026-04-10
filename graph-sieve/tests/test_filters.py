from graph_sieve.filters import is_domain_specific

def test_filter_generic():
    # Standard tech terms should be filtered out
    assert is_domain_specific("Docker") is False
    assert is_domain_specific("SQL") is False
    assert is_domain_specific("API") is False

def test_filter_specific():
    # Project-specific terms should pass
    assert is_domain_specific("N-RT-RIC") is True
    assert is_domain_specific("Cortex-AI") is True

def test_whitelist():
    # Whitelisted terms should pass even if in lexicon
    assert is_domain_specific("SQL", whitelist=["SQL"]) is True
    assert is_domain_specific("Cortex", whitelist=["Cortex"]) is True
