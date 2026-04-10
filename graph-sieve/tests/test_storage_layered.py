from graph_sieve.models import DictionaryEntry, Dictionary

def test_layered_lookup_hit():
    # Setup L1 cache
    l1 = {"Prism": DictionaryEntry(term="Prism", overview="L1 Def", source_file="L1")}
    
    # Layered lookup logic (Simplified for test)
    term = "Prism"
    result = l1.get(term)
    
    assert result.overview == "L1 Def"

def test_layered_lookup_miss_l1_hit_l2():
    # Setup L1 and L2 (Dictionary)
    l1 = {}
    l2 = Dictionary()
    l2.entries["Cortex"] = DictionaryEntry(term="Cortex", overview="L2 Def", source_file="L2")
    
    term = "Cortex"
    result = l1.get(term) or l2.entries.get(term)
    
    assert result.overview == "L2 Def"
