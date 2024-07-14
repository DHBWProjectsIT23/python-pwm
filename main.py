"""
Main entry point of the pokemon game
Sets the correct path for the module and test suit
"""

import os
import sys
from curses import wrapper

path = os.path.dirname(os.path.abspath(__file__))
sourcePath = os.path.join(path, "src")
sys.path.insert(0, sourcePath)

# pylint: disable=C0413 # Import must be placed after adding the correct path to sys.path
from test_module.placeholder import Placeholder
from tui.tui import tui_main

if __name__ == "__main__":
    Placeholder.main()
    wrapper(tui_main)
