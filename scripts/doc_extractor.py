import importlib
import inspect
import sys


def get_doc(obj_path):
    try:
        parts = obj_path.split('.')
        obj = None
        remaining_parts = parts

        # Try to find the longest importable module path
        for i in range(len(parts)):
            mod_name = '.'.join(parts[:i + 1])
            try:
                # Some modules might have side effects or be slow, but this is the way
                mod = importlib.import_module(mod_name)
                obj = mod
                remaining_parts = parts[i + 1:]
            except ImportError:
                break

        if obj is None:
            print(f"Error: Could not import any part of {obj_path}")
            return

        # Resolve remaining parts as attributes
        for part in remaining_parts:
            obj = getattr(obj, part)

        # Get signature if it's a function or class
        sig = ""
        # Handle properties or other non-callable but documented things
        if inspect.isfunction(obj) or inspect.isclass(obj) or inspect.ismethod(obj):
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = "(...)"
        elif hasattr(obj, '__call__') and not isinstance(obj, type):
            try:
                sig = str(inspect.signature(obj))
            except Exception:
                sig = "(...)"

        doc = inspect.getdoc(obj) or "No docstring available."

        print(f"### `{obj_path}{sig}`\n")
        print(f"{doc}\n")
        print("---")
    except Exception as e:
        print(f"Error fetching doc for {obj_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python doc_extractor.py module.submodule.function ...")
    else:
        for arg in sys.argv[1:]:
            get_doc(arg)
