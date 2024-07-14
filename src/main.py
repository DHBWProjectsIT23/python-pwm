"""
Main entry point of the pokemon game
Sets the correct path for the module and test suit
"""

import os
import sys
from curses import wrapper
from tui.tui import tui_main


def main() -> None:
    if len(sys.argv) > 1:
        cli_main()
    else:
        wrapper(tui_main)


def cli_main() -> None:
    print("Hello, World! - I am in CLI Mode")


if __name__ == "__main__":
    main()
