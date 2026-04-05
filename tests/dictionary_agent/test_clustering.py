import pytest
from src.dictionary_agent.graph_engine import GraphKnowledgeEngine
from src.dictionary_agent.models import Dictionary, GraphTriplet, DictionaryEntry
from unittest.mock import patch, MagicMock

def test_clustering_logic():
    engine = GraphKnowledgeEngine()
    # Create two separate communities
    rels = [
        GraphTriplet(subject="A", relationship="USES", object="B", anchor="...", source_file="..."),
        GraphTriplet(subject="B", relationship="USES", object="C", anchor="...", source_file="..."),
        GraphTriplet(subject="X", relationship="USES", object="Y", anchor="...", source_file="...")
    ]
    for r in rels: engine.add_triplet(r)
    
    communities = engine.cluster_communities()
    assert len(communities) == 2
    # Communities should be {A, B, C} and {X, Y}
    comm_sizes = [len(c) for c in communities]
    assert set(comm_sizes) == {2, 3}

def test_community_report_generation():
    engine = GraphKnowledgeEngine()
    engine.dictionary.entries["Prism"] = DictionaryEntry(term="Prism", definition="Security suite", source_file="...")
    engine.dictionary.entries["Cortex"] = DictionaryEntry(term="Cortex", definition="Identity", source_file="...")
    engine.add_triplet(GraphTriplet(subject="Prism", relationship="DEPENDS_ON", object="Cortex", anchor="...", source_file="..."))
    
    with patch("src.dictionary_agent.graph_engine.get_llm_client") as mock_client_factory:
        mock_client = MagicMock()
        mock_client.chat.return_value = "This is a summary of the security community."
        mock_client_factory.return_value = mock_client
        
        engine.generate_community_reports()
        
    assert len(engine.dictionary.community_reports) == 1
    report = engine.dictionary.community_reports[0]
    assert "security" in report.summary.lower()
    assert "Prism" in report.nodes
    assert "Cortex" in report.nodes
