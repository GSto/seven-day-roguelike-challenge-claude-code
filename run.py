#!/usr/bin/env python3
"""
Simple run script for development.
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Change to src directory and run the game
os.chdir(src_path)

try:
    from main import main
    main()
except ImportError as e:
    print(f"Error importing game modules: {e}")
    print("Make sure all dependencies are installed: uv sync")
    sys.exit(1)
except Exception as e:
    import traceback
    print(f"Error running game: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)