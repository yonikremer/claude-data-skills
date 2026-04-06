import importlib.util
import os
import shutil
import sys


SKILL_DEPENDENCIES = {
    "machine-learning": ["torch", "transformers"],
    "visualization": ["matplotlib", "plotly"],
    "data-analysis/geopandas": ["geopandas"],
    "data-sources/database-pro": ["sqlalchemy"],
    "unstructured-data-processing": ["pdfplumber", "docx", "pptx", "extract_msg"],
}


def is_skill_ready(skill_rel_path):
    """Checks if all dependencies for a given skill path are installed."""
    # Normalize path to use forward slashes for prefix matching
    skill_rel_path = skill_rel_path.replace('\\', '/')
    for skill_prefix, pkgs in SKILL_DEPENDENCIES.items():
        if skill_rel_path.startswith(skill_prefix):
            for pkg in pkgs:
                try:
                    if importlib.util.find_spec(pkg) is None:
                        return False, pkg
                except (ImportError, ValueError):
                    return False, pkg
    return True, None


def copy_skills_to_claude_home():
    """
    Copies the 'skills' directory from the installed package to ~/.claude/skills.
    This also handles the new Claude-compatible slash command wrappers.
    """
    try:
        # Determine the installed 'skills' package's location
        spec = importlib.util.find_spec("skills")
        if spec is None or spec.origin is None:
            # Fallback for local development
            potential_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'skills'))
            if os.path.exists(potential_path):
                source_path = potential_path
            else:
                print(f"Error: Could not find installed 'skills' package. Please ensure it's installed correctly.",
                      file=sys.stderr)
                sys.exit(1)
        else:
            # spec.origin is the path to __init__.py. The directory of that is the source_path.
            source_path = os.path.dirname(os.path.abspath(spec.origin))

        home_dir = os.path.expanduser("~")
        claude_dir = os.path.join(home_dir, '.claude')
        destination_path = os.path.join(claude_dir, 'skills')

        print(f"Setting up Claude skills in '{destination_path}'")

        if not os.path.exists(source_path):
            print(f"Error: Source skills directory '{source_path}' does not exist.", file=sys.stderr)
            sys.exit(1)

        if os.path.exists(destination_path):
            print(f"Updating existing destination directory: {destination_path}")
            shutil.rmtree(destination_path)

        os.makedirs(claude_dir, exist_ok=True)

        def ignore_func(directory, contents):
            # Calculate path relative to source_path for dependency check
            rel_dir = os.path.relpath(directory, source_path)
            ignored = []
            for item in contents:
                # Build the path of the current item relative to source_path
                if rel_dir == ".":
                    item_rel_path = item
                else:
                    item_rel_path = os.path.join(rel_dir, item)

                # Check dependencies for directories only
                if os.path.isdir(os.path.join(directory, item)):
                    ready, missing_pkg = is_skill_ready(item_rel_path)
                    if not ready:
                        print(f"  - Skipping skill '{item_rel_path}' (missing dependency: {missing_pkg})")
                        ignored.append(item)
            return ignored

        shutil.copytree(source_path, destination_path, ignore=ignore_func)
        print(f"Successfully copied skills and command wrappers.")

    except Exception as e:
        print(f"Error during Claude skills setup: {e}", file=sys.stderr)
        sys.exit(1)


def setup_gemini_commands():
    """
    Copies the '.toml' command files from the installed package to .gemini/commands
    in the current working directory for Gemini CLI users.
    """
    try:
        # Find the claude_data_skills package
        spec = importlib.util.find_spec("claude_data_skills")
        if spec is None or spec.origin is None:
            # Fallback for local development or if running from source
            potential_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'commands'))
            if os.path.exists(potential_path):
                commands_source = potential_path
            else:
                print(
                    "Warning: Could not find claude_data_skills package or local commands folder. Skipping Gemini setup.")
                return
        else:
            package_dir = os.path.dirname(os.path.abspath(spec.origin))
            commands_source = os.path.join(package_dir, 'commands')

        gemini_dest = os.path.join(os.getcwd(), '.gemini', 'commands')

        if not os.path.exists(commands_source):
            print(f"Warning: Commands source '{commands_source}' not found. Skipping Gemini setup.")
            return

        print(f"Setting up Gemini slash commands in '{gemini_dest}'")
        os.makedirs(gemini_dest, exist_ok=True)

        for filename in os.listdir(commands_source):
            if filename.endswith('.toml'):
                shutil.copy2(os.path.join(commands_source, filename), os.path.join(gemini_dest, filename))
                print(f"  - Copied {filename}")

        print("Gemini slash commands setup complete.")

    except Exception as e:
        print(f"Error during Gemini setup: {e}", file=sys.stderr)


def main():
    """Main entry point for setting up both Claude and Gemini environments."""
    print("--- Claude Data Skills Setup ---")
    copy_skills_to_claude_home()
    print("\n--- Gemini CLI Setup ---")
    setup_gemini_commands()
    print(
        "\nSetup complete! You can now use slash commands (/analyze, /explore, /query, etc.) in both Claude and Gemini.")


if __name__ == "__main__":
    main()
