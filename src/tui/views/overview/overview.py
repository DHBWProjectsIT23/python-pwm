import asyncio
import curses
from curses.panel import new_panel
from src.model.metadata import Metadata
from src.model.password import Password
from src.tui.views.overview.add_password_prompt import show_add_password_prompt
from src.tui.views.overview.create_password_prompt import PasswordCreator
from src.tui.views.overview.tabbar import Tabbar
from src.tui.panel import Panel
import sqlite3
import sys
from src.tui.views.overview.password_list import PasswordList
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
from src.controller.password import (
    insert_password_information,
    retrieve_password_information,
    update_password_information,
)
from src.tui.util import percentage_of

CONTROL_STR: str = """
- ⇆ Change Tab - q Quit -
""".strip()
PASS_CONTROL_STR: str = """
- ↑↓ Navigate Passwords - r Reveal Password - a Add New Password - ↩ Show More Information
""".strip()
# n - New Password - c Checl - C Check all


async def show_overview(
    window: Window, connection: sqlite3.Connection, cursor: sqlite3.Cursor, user: User
) -> None:
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

    passwords = retrieve_password_information(cursor, user)
    password_list = init_password_list(list_window, passwords)

    window.writeBottomCenterText(PASS_CONTROL_STR, (-1, 0))
    window.writeBottomCenterText(CONTROL_STR)

    window().refresh()

    # show_add_password_prompt(password_tab, passwords[0])

    while True:
        key_input: int = window().getch()
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
            case 65 | 97:
                password_information = password_list.get_selected()
                new_password = show_add_password_prompt(
                    password_tab, password_information
                )
                if new_password is not None:
                    password_information.add_password(
                        Password(new_password, Metadata())
                    )
                    update_password_information(cursor, password_information, user)
                    password_information.decrypt_data()
                    connection.commit()
                    password_list.refresh_selected()

                list_window().box()
                list_window().refresh()
                summary_window().box()
                summary_window().refresh()
                password_list.refresh()

            case 67:
                loading_message = "Loading..."
                loading_popup = create_centered_popup(
                    window, 5, len(loading_message) + 4
                )
                loading_popup().box()
                loading_popup.writeCenteredText(loading_message, (0, 0))
                loading_popup().refresh()
                await password_list.check_all()
            case 78 | 110:
                new_password = PasswordCreator(password_tab, user, cursor).run()
                if new_password is not None:
                    new_password = insert_password_information(cursor, new_password)
                    connection.commit()
                    new_password.decrypt_data()
                    password_list.add_item(new_password)

                list_window().box()
                list_window().refresh()
                summary_window().box()
                summary_window().refresh()
                password_list.refresh()

            case 99:
                await password_list.check_selected()

            case 81 | 113:
                sys.exit(0)
            case 82 | 114:
                password_list.toggle_selected()
