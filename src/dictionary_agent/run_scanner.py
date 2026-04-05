import argparse
import os

from src.dictionary_agent.agent import DictionaryAgent
from src.dictionary_agent.ai_discovery import get_extraction_prompt


def scan_network_drive(drive_path: str, dictionary_path: str = "dictionary.json"):
    """
    Scans a directory for PDF and PPTX files and processes them using the DictionaryAgent.
    """
    if not os.path.exists(drive_path):
        print(f"Error: Path '{drive_path}' does not exist.")
        return

    agent = DictionaryAgent(dictionary_path)

    files_to_process = []
    for root, _, files in os.walk(drive_path):
        for file in files:
            if file.lower().endswith((".pdf", ".pptx")):
                files_to_process.append(os.path.join(root, file))

    if not files_to_process:
        print(f"No PDF or PPTX files found in '{drive_path}'.")
        return

    print(f"Found {len(files_to_process)} files. Starting extraction...")

    for file_path in files_to_process:
        print(f"\nProcessing: {os.path.basename(file_path)}")
        try:
            # Step 1: Extract Text
            raw_text = agent.scan_file(file_path)

            if not raw_text or len(raw_text.strip()) < 10:
                print(f"Skipping {file_path}: No readable text found.")
                continue

            # Step 2: Prepare AI Prompt
            # In a real run, the AI (Gemini) would receive this prompt and return a JSON list of terms.
            existing_terms = list(agent.dictionary.entries.keys())
            prompt = get_extraction_prompt(raw_text, existing_terms)

            print("--- EXTRACTION PROMPT GENERATED ---")
            print("To complete the extraction, provide the text below to the AI:")
            print(f"(File: {os.path.basename(file_path)})")

            # Note: In an automated agentic flow, we would call the LLM API here.
            # Since this is a framework for the user, we output the prompt for the AI to handle.
            # If the user is running this IN this session, I (the AI) will handle the next step.

            # For now, we'll mark this as 'Ready for AI Discovery'.
            print("Status: Waiting for AI Discovery pass.")

        except Exception as e:
            print(f"Failed to process {file_path}: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Scan a network drive for technical terms.")
    parser.add_argument("path", help="Path to the network drive or local folder to scan.")
    parser.add_argument("--dict", default="dictionary.json", help="Path to the dictionary JSON file.")

    args = parser.parse_args()
    scan_network_drive(args.path, args.dict)


if __name__ == "__main__":
    main()
