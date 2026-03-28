import os
import shutil
import sys

def copy_skills_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    source_path = os.path.join(project_root, 'skills')

    print(f"DEBUG: Current working directory (script): {os.getcwd()}")
    print(f"DEBUG: Environment variable HOME: {os.environ.get('HOME', 'Not set')}")
    print(f"DEBUG: Environment variable USERPROFILE: {os.environ.get('USERPROFILE', 'Not set')}")
    print(f"DEBUG: Environment variable APPDATA: {os.environ.get('APPDATA', 'Not set')}")

    home_dir = os.path.expanduser("~")

    # --- DIAGNOSTIC: Attempt to create a simple test file in user's home ---
    test_file_path = os.path.join(home_dir, 'pip_install_test_file.txt')
    try:
        with open(test_file_path, 'w') as f:
            f.write("This file was created by the post-install script.
")
        print(f"DEBUG: Successfully created diagnostic file: {test_file_path}")
    except Exception as e:
        print(f"DEBUG: Failed to create diagnostic file at {test_file_path}: {e}", file=sys.stderr)
    # --- END DIAGNOSTIC ---

    claude_dir = os.path.join(home_dir, '.claude')
    destination_path = os.path.join(claude_dir, 'skills')

    print(f"DEBUG: Determined HOME directory (os.path.expanduser): {home_dir}")
    print(f"Attempting to copy skills from '{source_path}' to '{destination_path}'")

    if not os.path.exists(source_path):
        print(f"Error: Source skills directory '{source_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        if os.path.exists(claude_dir):
            print(f"DEBUG: .claude directory exists at: {claude_dir}")
            print(f"DEBUG: Contents of .claude directory before copy: {os.listdir(claude_dir)}")
        else:
            print(f"DEBUG: .claude directory does NOT exist at: {claude_dir}, will be created by os.makedirs")

        if os.path.exists(destination_path):
            print(f"Removing existing destination directory: {destination_path}")
            shutil.rmtree(destination_path)
            
        os.makedirs(claude_dir, exist_ok=True)
        shutil.copytree(source_path, destination_path)
        print(f"Successfully copied skills from '{source_path}' to '{destination_path}'")

        if os.path.exists(destination_path):
            print(f"DEBUG: Contents of '{destination_path}' after copy:")
            for item in os.listdir(destination_path):
                print(f"  - {item}")
        else:
            print(f"DEBUG: Destination path '{destination_path}' does not exist after copy.", file=sys.stderr)
        
        if os.path.exists(claude_dir):
            print(f"DEBUG: Final contents of .claude directory: {os.listdir(claude_dir)}")

    except Exception as e:
        print(f"Error copying skills folder: {e}", file=sys.stderr)
        sys.exit(1)

    print("DEBUG: Script finished executing.")


if __name__ == "__main__":
    copy_skills_folder()
