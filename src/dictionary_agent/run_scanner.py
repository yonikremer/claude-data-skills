import argparse
import os
import json
from src.dictionary_agent.agent import DictionaryAgent
from src.dictionary_agent.storage import save_dictionary

def run_local_agent(scan_path: str, dictionary_path: str = "GOLDEN_TERMS.json", 
                    seed_path: str = None, whitelist_path: str = None):
    """
    Runs the full Selective Knowledge Pipeline on a local directory.
    """
    if not os.path.exists(scan_path):
        print(f"Error: Scan path '{scan_path}' does not exist.")
        return

    # Load whitelist if provided
    whitelist = []
    if whitelist_path and os.path.exists(whitelist_path):
        with open(whitelist_path, "r", encoding="utf-8") as f:
            whitelist = [line.strip() for line in f if line.strip()]

    # Initialize Agent
    agent = DictionaryAgent(
        dictionary_path=dictionary_path,
        whitelist=whitelist,
        seed_paths=[seed_path] if seed_path else []
    )

    print(f"--- Starting Dictionary Agent ---")
    print(f"Target: {scan_path}")
    print(f"Dictionary: {dictionary_path}")
    if seed_path:
        print(f"Seeds: {seed_path}")

    # Process
    added_terms = agent.process_directory(scan_path)

    # Final summary of dictionary
    print(agent.generate_summary())
    
    # Save one last time to be sure
    save_dictionary(agent.dictionary, dictionary_path)
    print(f"Dictionary saved to {dictionary_path}")

def main():
    parser = argparse.ArgumentParser(description="Run the Selective Knowledge Dictionary Agent locally.")
    parser.add_argument("path", help="Path to the directory to scan.")
    parser.add_argument("--dict", default="GOLDEN_TERMS.json", help="Output path for the dictionary JSON.")
    parser.add_argument("--seed", help="Optional path to 'Seed' documents (high-authority).")
    parser.add_argument("--whitelist", help="Optional path to a whitelist of terms to always include.")

    args = parser.parse_args()
    run_local_agent(args.path, args.dict, args.seed, args.whitelist)

if __name__ == "__main__":
    main()
