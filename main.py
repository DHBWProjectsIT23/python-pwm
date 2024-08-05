import sys
import os
import sqlite3
from curses import wrapper

# Add the src directory to the Python path
path = os.path.dirname(os.path.abspath(__file__))
sourcePath = os.path.join(path, "src")
sys.path.insert(0, sourcePath)

# pylint: disable=C0413 # Import must be placed after adding the correct path to sys.path
from src.model.password import (
    Password,
    adapt_password,
    convert_password,
)

from src.tui import tui
from src.cli import cli

if __name__ == "__main__":
    sqlite3.register_converter("password", convert_password)
    sqlite3.register_adapter(Password, adapt_password)
    if len(sys.argv) > 1:
        cli.main()
    else:
        wrapper(tui.main)
