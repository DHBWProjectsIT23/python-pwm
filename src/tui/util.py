import curses
import sys
import itertools
import time
from typing import TYPE_CHECKING
from .window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


def init_tui(stdscr: CursesWindow) -> Window:
    stdscr.clear()
    curses.noecho()
    curses.curs_set(False)
    _init_colors(stdscr)
    return Window(stdscr)


def _init_colors(stdscr: CursesWindow) -> None:
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.clear()


def print_centered_logo(window: Window, offset: tuple[int, int]) -> None:
    logo: str = """
██████  ██████  ██     ██ ███    ███
██   ██ ██   ██ ██     ██ ████  ████
██████  ██████  ██  █  ██ ██ ████ ██
██      ██      ██ ███ ██ ██  ██  ██
██      ██       ███ ███  ██      ██
 """.strip()
    logo_caption = " Python Password Manager "

    window.writeCenteredMultilineText(logo, offset, curses.color_pair(5))
    window.writeCenteredText(
        logo_caption, (-5, 0), curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE
    )
    window().refresh()


def percentage_of(percentage: int, whole: int) -> int:
    return int((whole / 100) * percentage)


def shorten_str(text: str, length: int, substitute: str = "...") -> str:
    str_len = length - len(substitute)
    return text[:str_len] + substitute


def pad_with(text: str, length: int, padding: str = " ") -> str:
    return text + (length - len(text)) * padding


def no_space_validator(ch: int) -> int:
    if ch == 12:
        sys.exit(1)
    if ch == 32:
        return 0

    return ch
