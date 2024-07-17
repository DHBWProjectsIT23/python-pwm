import curses
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
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.clear()
