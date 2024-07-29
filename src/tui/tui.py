import asyncio
from typing import TYPE_CHECKING

from src.controller.connection import connect_to_db

from .util import init_tui
from .views.login import show_login
from .views.start import show_start
from .views.overview import show_overview
from .window import Window
import time
import curses

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


def tui_main(stdscr: CursesWindow) -> None:
    start_tui(stdscr)


def start_tui(stdscr: CursesWindow) -> None:
    window: Window = init_tui(stdscr)
    connection, cursor = connect_to_db("test.db")

    # choice = show_start(window)
    # window().clear()
    # if choice == 1:
    user = show_login(window, cursor)
    # elif choice == 2:
    #     raise NotImplementedError
    # else:
    #     raise ValueError("Unexpted choice")
    # time.sleep(1)
    window().clear()
    show_overview(window, cursor, user)

    window().clear()
