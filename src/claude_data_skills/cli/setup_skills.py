import os
import shutil
import sys
import importlib.util

def copy_skills_to_claude_home():
    """
    Copies the 'skills' directory from the installed package to ~/.claude/skills.
    """
    try:
        # Determine the installed 'skills' package's location
        spec = importlib.util.find_spec("skills")
        if spec is None or spec.origin is None:
            print(f"Error: Could not find installed 'skills' package. Please ensure it's installed correctly.", file=sys.stderr)
            sys.exit(1)

        # spec.origin is the path to __init__.py. The directory of that is the source_path.
        source_path = os.path.dirname(os.path.abspath(spec.origin))

        home_dir = os.path.expanduser("~")
        claude_dir = os.path.join(home_dir, '.claude')
        destination_path = os.path.join(claude_dir, 'skills')

        print(f"Attempting to copy skills from '{source_path}' to '{destination_path}'")

        if not os.path.exists(source_path):
            print(f"Error: Source skills directory '{source_path}' does not exist (installed 'skills' package not found).", file=sys.stderr)
            sys.exit(1)

        if os.path.exists(destination_path):
            print(f"Removing existing destination directory: {destination_path}")
            shutil.rmtree(destination_path)
        
        os.makedirs(claude_dir, exist_ok=True)
        shutil.copytree(source_path, destination_path)
        print(f"Successfully copied skills from '{source_path}' to '{destination_path}'")
        print("Setup complete. You can now use the Claude data skills.")

    except Exception as e:
        print(f"Error during skills setup: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    copy_skills_to_claude_home()
