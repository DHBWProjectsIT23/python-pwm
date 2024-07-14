import sys
import pickle
from curses import wrapper
from tui.tui import tui_main


def main() -> None:
    if len(sys.argv) > 1:
        cli_main()
    else:
        wrapper(tui_main)


def cli_main() -> None:
    print("Hello, World! - I am in CLI Mode")
    print("Reading pickle test")


if __name__ == "__main__":
    main()
