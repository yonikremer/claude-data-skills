import os
import tempfile
from pathlib import Path
from collections import Counter, deque
from itertools import islice, chain, groupby
from contextlib import ExitStack, suppress
from functools import lru_cache, partial
from dataclasses import dataclass, field, asdict
import bisect
import heapq

def test_pathlib():
    print("Testing Pathlib...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello", encoding='utf-8')
        
        # Atomic write pattern
        tmp_file = test_file.with_suffix('.tmp')
        tmp_file.write_text("world", encoding='utf-8')
        tmp_file.replace(test_file)
        assert test_file.read_text() == "world"
        
        # Stem and Suffix
        new_file = test_file.with_stem("new").with_suffix(".md")
        assert new_file.name == "new.md"
        print("Pathlib: OK")

def test_collections():
    print("Testing Collections...")
    counts = Counter(['a', 'b', 'a', 'c'])
    assert counts['a'] == 2
    
    d = deque(maxlen=2)
    d.append(1)
    d.append(2)
    d.append(3)
    assert list(d) == [2, 3]
    print("Collections: OK")

def test_itertools():
    print("Testing Itertools...")
    combined = list(chain([1, 2], [3, 4]))
    assert combined == [1, 2, 3, 4]
    
    subset = list(islice(range(100), 5, 8))
    assert subset == [5, 6, 7]
    
    data = [{'k': 'a', 'v': 1}, {'k': 'a', 'v': 2}, {'k': 'b', 'v': 3}]
    # Note: groupby needs sorted data
    groups = {k: len(list(g)) for k, g in groupby(data, key=lambda x: x['k'])}
    assert groups == {'a': 2, 'b': 1}
    print("Itertools: OK")

def test_contextlib():
    print("Testing Contextlib...")
    with suppress(FileNotFoundError):
        os.remove('non_existent_random_file_12345.txt')
    
    with ExitStack():
        # Just testing the stack mechanism
        pass
    print("Contextlib: OK")

def test_functools():
    print("Testing Functools...")
    @lru_cache()
    def add(a, b): return a + b
    assert add(1, 2) == 3
    
    plus_ten = partial(add, 10)
    assert plus_ten(5) == 15
    print("Functools: OK")

def test_dataclasses():
    print("Testing Dataclasses...")
    @dataclass
    class Item:
        name: str
        tags: list = field(default_factory=list)
    
    i = Item("test")
    assert i.tags == []
    assert asdict(i) == {"name": "test", "tags": []}
    print("Dataclasses: OK")

def test_performance_tools():
    print("Testing Performance Tools...")
    my_list = [10, 20, 30]
    bisect.insort(my_list, 25)
    assert my_list == [10, 20, 25, 30]
    
    data = [1, 5, 2, 8, 3]
    assert heapq.nlargest(2, data) == [8, 5]
    print("Performance Tools: OK")

if __name__ == "__main__":
    test_pathlib()
    test_collections()
    test_itertools()
    test_contextlib()
    test_functools()
    test_dataclasses()
    test_performance_tools()
    print("\nAll tests passed!")
