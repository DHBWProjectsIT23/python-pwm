import asyncio
import sqlite3
import time
from typing import TYPE_CHECKING

from src.controller.connection import DB_PATH, connect_to_db

from .util import init_tui
from .views.login import show_login
from .views.overview import show_overview
from .window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


def main(stdscr: CursesWindow) -> None:
    with connect_to_db(DB_PATH) as connection:
        asyncio.run(run_tui(stdscr, connection, connection.cursor))


async def run_tui(
    stdscr: CursesWindow, connection: sqlite3.Connection, cursor: sqlite3.Cursor
) -> None:
    window: Window = init_tui(stdscr)

    height, width = window.getSize()
    window().refresh()

    to_small = False
    if height < 30 or width < 80:
        to_small = True

    while to_small:
        # height_2, width_2 = window.getSize()
        # if height_2 != height or width_2 != width:
        height, width = window.getSize()
        window().clear()
        window.writeCenteredText(f"Your terminal size {width}x{height} is too small")
        window().refresh()
        if height >= 30 and width >= 80:
            to_small = False

        time.sleep(0.1)

    window().clear()

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
