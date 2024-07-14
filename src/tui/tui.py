import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


def tui_main(stdscr: Window) -> None:
    stdscr.clear()

    stdscr.addstr(10, 20, "Hello, World!")

    stdscr.refresh()
    stdscr.getkey()
