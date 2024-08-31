"""
Main entry point for the application.

This script initializes the application by setting up the necessary environment,
registering SQLite converters and adapters, and then launching either the CLI or
TUI (Text User Interface) based on the presence of command-line arguments.
"""

import os
import sqlite3
import sys
from curses import wrapper

from dotenv import load_dotenv

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

if __name__ == "__main__":
    sqlite3.register_converter("password", convert_password)
    sqlite3.register_adapter(Password, adapt_password)
    load_dotenv()
    wrapper(tui.main)
