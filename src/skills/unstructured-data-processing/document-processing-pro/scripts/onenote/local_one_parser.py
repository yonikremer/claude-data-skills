from markitdown import MarkItDown
import os
import sys

def parse_one_file(file_path, output_md=None):
    """
    Parses a local .one file into Markdown using Microsoft's MarkItDown library.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    md = MarkItDown()
    
    try:
        print(f"Converting '{file_path}' to Markdown...")
        result = md.convert(file_path)
        content = result.text_content
        
        if output_md:
            with open(output_md, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully saved to '{output_md}'")
        else:
            print("--- Extracted Content ---")
            print(content)
            print("--- End of Content ---")
            
    except Exception as e:
        print(f"Failed to parse OneNote file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python local_one_parser.py <path_to_one_file> [output_file.md]")
        sys.exit(1)
    
    one_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    parse_one_file(one_file, output_file)
