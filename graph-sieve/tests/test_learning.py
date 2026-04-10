from graph_sieve.discovery import process_discovered_terms
from graph_sieve.models import Dictionary

def test_new_term_discovery():
    dictionary = Dictionary()
    discovered = [{"term": "New Term", "overview": "New Overview", "deep_dive": "New Deep Dive", "anchor": "Found in context"}]
    process_discovered_terms(discovered, dictionary, "file.pdf")

    assert "New Term" in dictionary.entries
    assert dictionary.entries["New Term"].overview == "New Overview"
    assert dictionary.entries["New Term"].deep_dive == "New Deep Dive"
    assert len(dictionary.entries["New Term"].usage_examples) == 1

def test_existing_term_enrichment():
    dictionary = Dictionary()
    # Add initial term
    initial_discovered = [{"term": "Old Term", "overview": "Old Overview", "anchor": "First found"}]
    process_discovered_terms(initial_discovered, dictionary, "first.pdf")

    # Enrichment - should add second example and update deep_dive if missing
    new_discovered = [{"term": "Old Term", "overview": "Old Overview", "deep_dive": "New Deep Dive", "anchor": "Second found"}]
    process_discovered_terms(new_discovered, dictionary, "second.pdf")

    assert len(dictionary.entries["Old Term"].usage_examples) == 2
    assert dictionary.entries["Old Term"].usage_examples[0].source == "first.pdf"
    assert dictionary.entries["Old Term"].usage_examples[1].source == "second.pdf"
    assert dictionary.entries["Old Term"].deep_dive == "New Deep Dive"
