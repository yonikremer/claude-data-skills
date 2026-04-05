from src.dictionary_agent.storage import LayeredDictionary, DictionaryEntry

def test_layered_lookup_hit():
    # Setup L1 cache
    l1 = {"Prism": DictionaryEntry(term="Prism", definition="L1 Def", source_file="L1")}
    layered = LayeredDictionary(l1_cache=l1)
    
    # Should find in L1
    entry = layered.get_entry("Prism")
    assert entry.definition == "L1 Def"

def test_layered_lookup_miss_l1_hit_l2():
    # Setup L1 and L2 (Dictionary)
    l1 = {}
    from src.dictionary_agent.models import Dictionary
    l2 = Dictionary()
    l2.entries["Cortex"] = DictionaryEntry(term="Cortex", definition="L2 Def", source_file="L2")
    
    layered = LayeredDictionary(l1_cache=l1, l2_store=l2)
    
    # Miss L1, Hit L2
    entry = layered.get_entry("Cortex")
    assert entry.definition == "L2 Def"
