import importlib
import inspect
from pathlib import Path
from typing import List

# Get the directory containing this __init__.py file
_tools_dir = Path(__file__).parent

# Dynamically discover and import all tool functions
_discovered_tools = {}
__all__: List[str] = []

for py_file in _tools_dir.glob("*.py"):
    # Skip __init__.py and private files
    if py_file.name.startswith("_"):
        continue

    # Import the module
    module_name = py_file.stem
    try:
        module = importlib.import_module(f".{module_name}", package=__package__)

        # Find all callable functions in the module (exclude private functions)
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith("_") and obj.__module__ == module.__name__:
                _discovered_tools[name] = obj
                __all__.append(name)
                # Add to current namespace for imports
                globals()[name] = obj

    except ImportError as e:
        print(f"Warning: Could not import {module_name}: {e}")

# Sort __all__ for consistent ordering
__all__.sort()
