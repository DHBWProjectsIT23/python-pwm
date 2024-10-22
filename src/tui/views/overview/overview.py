"""
Module for managing and displaying the overview screen with tabbed interface
in a terminal-based user interface for a password manager application.
"""

import curses
import sqlite3
import sys
from typing import Optional

import _curses

from src.model.user import User
from src.tui.keys import Keys
from src.tui.util import generate_control_str
from src.tui.util import percentage_of
from src.tui.util import validate_size
from src.tui.views.overview.components.tab_interface import TabInterface
from src.tui.views.overview.components.tabbar import Tabbar
from src.tui.views.overview.io_tab.io_tab import IoTab
from src.tui.views.overview.password_tab.password_tab import PasswordTab
from src.tui.views.overview.user_tab.user_tab import UserTab
from src.tui.window import Window

CONTROLS: dict[str, str] = {"⇆": "Change Tab", "q": "Quit"}


async def show_overview(
    window: Window, connection: sqlite3.Connection, user: User, current_tab: int
) -> int:
    """
    Displays the overview screen with multiple tabs. Handles user input to navigate
    between tabs and process tab-specific actions.

    Args:
        window (Window): The Window object used for displaying the overview screen.
        connection (sqlite3.Connection): The database connection for interacting with the database.
        user (User): The current user for whom the overview is displayed.
        current_tab (int): The index of the currently selected tab.

    Returns:
        int: An integer representing the result of the operation,
        typically the index of the selected tab or 0 if an error occurs.

    Exits:
        sys.exit(0) if the user presses 'q' or 'Q'.
    """
    curses.curs_set(False)
    screen_size = window.get_size()
    y_start = max(percentage_of(15, screen_size[0]), 5)

    window_size = screen_size[0] - y_start - 1, screen_size[1] - 2

    try:
        password_tab = PasswordTab(window_size, y_start, user, connection)
        user_tab = UserTab(window_size, y_start, user, connection)
        io_tab = IoTab(window_size, y_start, user, connection)
    except _curses.error:
        return 0

    tabs = {"Passwords": password_tab, "User": user_tab, "Import/Export": io_tab}

    result = check_size(window, None, screen_size)
    if result is not None:
        return result
    _, tabbar = init_top_window(window, screen_size, tabs, current_tab)

    window.write_bottom_center_text(generate_control_str(CONTROLS))

    result = check_size(window, tabbar, screen_size)
    if result is not None:
        return result
    window().refresh()
    tabbar.refresh()

    while True:
        curses.curs_set(False)
        window().timeout(1000)
        input_key: int = window().getch()
        window().timeout(-1)
        match input_key:
            case -1:
                pass
            case Keys.TAB:
                tabbar.next_tab()
            case Keys.Q | Keys.Q_LOWER:
                sys.exit(0)
            case _:
                current_tab = tabbar.selected
                match current_tab:
                    case 0:
                        await password_tab.process_input(input_key)
                    case 1:
                        await user_tab.process_input(input_key)
                    case 2:
                        await io_tab.process_input(input_key)

        result = check_size(window, tabbar, screen_size)
        if result is not None:
            return result


def check_size(
    window: Window, tabbar: Optional[Tabbar], screen_size: tuple[int, int]
) -> Optional[int]:
    """
    Checks if the window size has changed and validates the size if needed.

    Args:
        window (Window): The Window object to check the size of.
        tabbar (Optional[Tabbar]): The Tabbar object to return the selected tab index if needed.
        screen_size (tuple[int, int]): The current size of the screen.

    Returns:
        Optional[int]: The index of the selected tab if the size has changed, otherwise None.
    """
    if screen_size != window.get_size():
        validate_size(window)
        return tabbar.selected if tabbar else 0
    return None


def init_top_window(
    parent: Window,
    screen_size: tuple[int, int],
    tabs: dict[str, TabInterface],
    current_tab: int,
) -> tuple[Window, Tabbar]:
    """
    Initializes the top window and the tab bar for the overview screen.

    Args:
        parent (Window): The parent Window object to derive the top window from.
        screen_size (tuple[int, int]): The size of the screen.
        tabs (dict[str, TabInterface]):
        A dictionary of tabs and their corresponding TabInterface objects.
        current_tab (int): The index of the currently selected tab.

    Returns:
        tuple[Window, Tabbar]: A tuple containing the top Window object and the Tabbar object.
    """
    top_window_height = max(percentage_of(15, screen_size[0]) - 1, 4)
    top_window = Window(
        parent().derwin(
            top_window_height,
            screen_size[1] - 2,
            1,
            1,
        )
    )
    top_window().box()

    top_window().addstr(1, 1, "PPWM", curses.A_BOLD | curses.color_pair(5))
    top_window().addstr(" - Python Password Manager")

    tabbar = Tabbar(top_window, tabs, (top_window_height - 2, 0))
    tabbar.selected = current_tab

    top_window().refresh()
    return top_window, tabbar
