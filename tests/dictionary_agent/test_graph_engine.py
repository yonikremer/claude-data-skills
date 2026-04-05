import pytest
from src.dictionary_agent.graph_engine import GraphKnowledgeEngine
from src.dictionary_agent.models import Dictionary, GraphTriplet

def test_add_triplet():
    engine = GraphKnowledgeEngine()
    triplet = GraphTriplet(
        subject="Prism",
        relationship="SUB_PROJECT_OF",
        object="Security-Suite",
        anchor="Prism is part of Security-Suite",
        source_file="test.txt"
    )
    engine.add_triplet(triplet)
    
    assert len(engine.dictionary.relationships) == 1
    assert engine.dictionary.relationships[0].subject == "Prism"

def test_duplicate_triplet():
    engine = GraphKnowledgeEngine()
    triplet = GraphTriplet(
        subject="Prism",
        relationship="SUB_PROJECT_OF",
        object="Security-Suite",
        anchor="...",
        source_file="test.txt"
    )
    engine.add_triplet(triplet)
    engine.add_triplet(triplet) # Exact duplicate
    
    assert len(engine.dictionary.relationships) == 1

def test_get_context_map():
    engine = GraphKnowledgeEngine()
    triplet = GraphTriplet(
        subject="Prism",
        relationship="SUB_PROJECT_OF",
        object="Security-Suite",
        anchor="...",
        source_file="test.txt"
    )
    engine.add_triplet(triplet)
    
    context = engine.get_context_map("Prism")
    assert "SUB_PROJECT_OF" in context
    assert "Security-Suite" in context
