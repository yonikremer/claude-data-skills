import pytest
from src.dictionary_agent.models import Dictionary, DictionaryEntry
from src.dictionary_agent.ai_discovery import process_discovered_terms

def test_new_term_discovery():
    dictionary = Dictionary()
    discovered = [{"term": "New Term", "definition": "New Definition", "usage_context": "Found in context"}]
    process_discovered_terms(discovered, dictionary, "file.pdf")
    
    assert "New Term" in dictionary.entries
    assert dictionary.entries["New Term"].definition == "New Definition"
    assert len(dictionary.entries["New Term"].usage_examples) == 1

def test_existing_term_enrichment():
    dictionary = Dictionary()
    # Add initial term
    initial_discovered = [{"term": "Old Term", "definition": "Old Definition", "usage_context": "First found"}]
    process_discovered_terms(initial_discovered, dictionary, "first.pdf")
    
    # Enrichment
    new_discovered = [{"term": "Old Term", "definition": "Updated Definition", "usage_context": "Second found"}]
    process_discovered_terms(new_discovered, dictionary, "second.pdf")
    
    assert len(dictionary.entries["Old Term"].usage_examples) == 2
    assert dictionary.entries["Old Term"].usage_examples[0].source == "first.pdf"
    assert dictionary.entries["Old Term"].usage_examples[1].source == "second.pdf"
