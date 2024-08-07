import curses
from src.model.password_information import PasswordInformation
from src.tui.views.overview.io_tab.io_tab import IoTab
from src.tui.views.overview.password_tab.password_tab import PasswordTab
import sqlite3
import sys
from src.tui.keys import Keys
from src.tui.views.overview.init_overview import (
    init_top_window,
)
from src.tui.window import Window
from src.model.user import User
from src.controller.password import (
    retrieve_password_information,
)
from src.tui.util import generate_control_str, percentage_of
from src.tui.views.overview.user_tab.user_tab import UserTab

CONTROLS: dict[str, str] = {"⇆": "Change Tab", "q": "Quit"}


async def show_overview(
    window: Window, connection: sqlite3.Connection, cursor: sqlite3.Cursor, user: User
) -> None:
    curses.curs_set(False)
    screen_size = window.getSize()
    y_start = percentage_of(15, screen_size[0])

    window_size = screen_size[0] - y_start - 1, screen_size[1] - 2

    passwords = retrieve_password_information(cursor, user)
    passwords = list(
        filter(PasswordInformation.create_password_filter("www.github.com"), passwords)
    )

    password_tab = PasswordTab(window_size, y_start, user, connection)
    user_tab = UserTab(window_size, y_start, user, connection)
    io_tab = IoTab(window_size, y_start, user, connection)

    tabs = {"Passwords": password_tab, "User": user_tab, "Import/Export": io_tab}

    top_window, tabbar = init_top_window(window, screen_size, tabs)

    window.writeBottomCenterText(generate_control_str(CONTROLS))

    window().refresh()
    password_tab.refresh()

    # tabbar.next_tab()

    while True:
        input_key: int = window().getch()
        match input_key:
            case Keys.TAB:
                tabbar.next_tab()
            case Keys.Q | Keys.q:
                sys.exit(0)
            case _:
                current_tab = tabbar.selected
                match current_tab:
                    case 0:
                        await password_tab.process_input(input_key)
                    case 1:
                        await user_tab.process_input(input_key)
                    case 2:
                        await io_tab.proccess_input(input_key)
