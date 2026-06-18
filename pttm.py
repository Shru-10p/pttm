import sys
import os

# Ensure the root directory is in the Python path so the package imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pttm.app import main

if __name__ == "__main__":
    main()
