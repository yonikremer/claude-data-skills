from graph_sieve.graph_engine import GraphKnowledgeEngine
from graph_sieve.models import GraphTriplet, DictionaryEntry

def test_clustering_logic():
    engine = GraphKnowledgeEngine()
    # Create two separate communities
    # Note: Using ALIAS_OF and SUB_PROJECT_OF which have weights > 0.4 threshold
    rels = [
        GraphTriplet(subject="A", relationship="ALIAS_OF", object="B", anchor="A is B", source_file="..."),
        GraphTriplet(subject="B", relationship="SUB_PROJECT_OF", object="C", anchor="B is part of C", source_file="..."),
        GraphTriplet(subject="X", relationship="ALIAS_OF", object="Y", anchor="X is Y", source_file="...")
    ]
    for r in rels: engine.add_triplet(r)

    communities = engine.cluster_communities(prune_threshold=0.1) # Lower threshold for test
    assert len(communities) == 2

def test_community_report_generation():
    engine = GraphKnowledgeEngine()
    engine.dictionary.entries["Prism"] = DictionaryEntry(term="Prism", overview="Security suite", source_file="...")
    engine.dictionary.entries["Cortex"] = DictionaryEntry(term="Cortex", overview="Identity manager", source_file="...")
    
    rel = GraphTriplet(subject="Prism", relationship="DEPENDS_ON", object="Cortex", anchor="Prism depends on Cortex", source_file="...")
    engine.add_triplet(rel)
    
    # This will still call LLM but we check if it handles the dictionary entries correctly
    # If MOCK_LLM is true, it should return a mock report
    engine.generate_community_reports()
    assert len(engine.dictionary.community_reports) > 0
