import sys
import os
from .storage import load_dictionary
from .graph_engine import GraphKnowledgeEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: dictionary-visualize <dictionary_json_path> [output_html_path]")
        print("Default output: graph.html")
        sys.exit(1)

    dict_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "graph.html"

    if not os.path.exists(dict_path):
        print(f"Error: Dictionary file '{dict_path}' not found.")
        sys.exit(1)

    print(f"Loading dictionary from {dict_path}...")
    dictionary = load_dictionary(dict_path)
    
    print("Initializing Graph Engine...")
    engine = GraphKnowledgeEngine(dictionary)
    
    print("Generating interactive visualization...")
    engine.visualize_graph(output_path)

if __name__ == "__main__":
    main()
