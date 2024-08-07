import asyncio
import sqlite3
import time
from typing import TYPE_CHECKING

from src.controller.connection import connect_to_db
from src.model.user import User

from .util import init_tui
from .views.start import show_start
from .views.login import show_login
from .views.registration import show_registration
from .views.overview.overview import show_overview
from .window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


def main(stdscr: CursesWindow) -> None:
    """
    Entry point for the application. Initializes the TUI and database connection,
    then starts the asynchronous event loop to run the TUI interface.

    Args:
        stdscr (CursesWindow): The standard curses window object used for drawing
                               the user interface.
    """
    with connect_to_db() as connection:
        asyncio.run(run_tui(stdscr, connection, connection.cursor()))


async def run_tui(
    stdscr: CursesWindow, connection: sqlite3.Connection, cursor: sqlite3.Cursor
) -> None:
    """
    Runs the terminal user interface (TUI) in an asynchronous context. Handles
    terminal size validation and UI initialization. Displays the overview screen
    after validating user credentials.

    Args:
        stdscr (CursesWindow): The standard curses window object used for drawing
                               the user interface.
        connection (sqlite3.Connection): The database connection used for data
                                         operations.
        cursor (sqlite3.Cursor): The database cursor used for querying and
                                 executing commands.

    Raises:
        Exception: If any unexpected errors occur during TUI operations or database
                   interactions.
    """
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

    choice = show_start(window)
    window().clear()
    if choice == 1:
        user = show_login(window, cursor)

    elif choice == 2:
        user = show_registration(window, connection, cursor)
    else:
        raise ValueError("Unexpted choice")

    # user = User.new("admin", "admin")
    # user.set_clear_username("admin")
    # user.set_clear_password("admin")
    assert user.has_clear_password(), "Error during login"
    assert user.has_clear_username(), "Error during login"

    # user = User.new("test", "test")
    # user.set_clear_password("test")

    window().clear()
    await show_overview(window, connection, cursor, user)

    window().clear()
