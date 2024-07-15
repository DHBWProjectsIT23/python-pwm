import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


def init_tui(stdscr: Window) -> None:
    stdscr.clear()
    curses.noecho()
    curses.curs_set(False)
    _init_colors()


def _init_colors() -> None:
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)


def get_screen_size(window: Window) -> tuple[int, int]:
    return window.getmaxyx()


def print_line_in_middle(window: Window, text: str) -> None:
    height, width = get_screen_size(window)
    window.addstr(height // 2 - 1, width // 2 - len(text) // 2, text)
