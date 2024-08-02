import asyncio
import curses
from src.tui.components.tabbar import Tabbar
from src.tui.panel import Panel
import sqlite3
import sys
from src.tui.components.password_list import PasswordList
from src.tui.popup import create_centered_popup
from src.tui.views.overview.init_overview import (
    init_io_tab,
    init_password_list,
    init_password_tab,
    init_top_window,
    init_user_tab,
)
from src.tui.window import Window
from src.model.user import User
from src.controller.password import retrieve_password_information
from src.tui.util import percentage_of

CONTROL_STR: str = """
- ⇆ Change Tab - q Quit -
""".strip()
PASS_CONTROL_STR: str = """
- ↑↓ Navigate Passwords - r Reveal Password - ↩ Show More Information
"""


async def show_overview(window: Window, cursor: sqlite3.Cursor, user: User) -> None:
    curses.curs_set(False)
    screen_size = window.getSize()
    main_y_start = percentage_of(15, screen_size[0])

    main_window_size = screen_size[0] - main_y_start - 2, screen_size[1] - 2

    password_tab, list_window, summary_window = init_password_tab(
        main_window_size, main_y_start
    )
    user_tab = init_user_tab(main_window_size, main_y_start)
    io_tab = init_io_tab(main_window_size, main_y_start)

    tabs = {"Passwords": password_tab, "User": user_tab, "Import/Export": io_tab}

    top_window, tabbar = init_top_window(window, screen_size, tabs)

    passwords = retrieve_password_information(cursor, user.username)
    password_list = init_password_list(list_window, passwords)

    window.writeCenteredText(CONTROL_STR, (window.getSize()[0] // 2, 0))
    window().refresh()

    await password_event_loop(window, password_tab, password_list, tabbar)


async def password_event_loop(
    window: Window,
    password_tab: Panel,
    password_list: PasswordList,
    tabbar: Tabbar,
) -> None:
    while True:
        key_input: int = window().getch()
        window().addstr(5, 5, f"{key_input}")
        window().refresh()
        match key_input:
            case 9:
                tabbar.next_tab()
                if not password_tab().hidden():
                    password_list.refresh()
            case curses.KEY_DOWN:
                # password_list.scroll_down()
                password_list.select_next()
            case curses.KEY_UP:
                # password_list.scroll_up()
                password_list.select_previous()
            case 67:
                loading_message = "Loading..."
                loading_popup = create_centered_popup(
                    window, 5, len(loading_message) + 4
                )
                loading_popup().box()
                loading_popup.writeCenteredText(loading_message, (0, 0))
                loading_popup().refresh()
                await password_list.check_all()
            case 99:
                await password_list.check_selected()

            case 81 | 113:
                sys.exit(0)
            case 82 | 114:
                password_list.toggle_selected()


def run_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
