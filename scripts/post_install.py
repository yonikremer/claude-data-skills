import os
import shutil
import sys

def copy_skills_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..')) # Adjust for 'scripts' directory
    source_path = os.path.join(project_root, 'skills')

    home_dir = os.path.expanduser("~")
    destination_path = os.path.join(home_dir, '.claude', 'skills')

    print(f"Attempting to copy skills from '{source_path}' to '{destination_path}'")

    if not os.path.exists(source_path):
        print(f"Error: Source skills directory '{source_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        # Remove destination if it exists to ensure a clean copy
        if os.path.exists(destination_path):
            print(f"Removing existing destination directory: {destination_path}")
            shutil.rmtree(destination_path)
            
        os.makedirs(os.path.dirname(destination_path), exist_ok=True) # Ensure parent directory exists
        shutil.copytree(source_path, destination_path)
        print(f"Successfully copied skills from '{source_path}' to '{destination_path}'")
    except Exception as e:
        print(f"Error copying skills folder: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    copy_skills_folder()
