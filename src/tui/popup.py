import curses
from curses.textpad import Textbox, rectangle
from .util import get_screen_size
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


def create_centered_popup(window: Window, height: int, width: int) -> Window:
    screen_height, scree_width = get_screen_size(window)
    y = (screen_height // 2) - (height // 2)
    x = (scree_width // 2) - (width // 2)
    return create_popup(window, y, x, height, width)


def create_popup(window: Window, y: int, x: int, height: int, width: int) -> Window:
    popup_window = window.derwin(height, width, y, x)
    return popup_window
