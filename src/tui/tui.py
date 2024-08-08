import asyncio
import sqlite3
from typing import TYPE_CHECKING

from src.controller.connection import connect_to_db
from .util import init_tui
from .util import validate_size
from .views.login import show_login
from .views.overview.overview import show_overview
from .views.registration import show_registration
from .views.start import show_start
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

    validate_size(window)
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

    current_tab = 0
    while True:
        window().clear()
        current_tab = await show_overview(window, connection, user, current_tab)
