import curses
from curses import panel
import sqlite3
import sys
from src.tui.window import Window
from src.tui.panel import Panel
from src.tui.components.tabbar import Tabbar
from src.model.user import User
from src.controller.password import retrieve_password_information


def show_overview(window: Window, cursor: sqlite3.Cursor, user: User) -> None:
    curses.curs_set(False)
    screen_height, screen_width = window.getSize()
    main_y_start = percentage(15, screen_height)

    main_window_height = screen_height - main_y_start - 1
    main_window_width = screen_width - 2

    password_tab = Panel(
        panel.new_panel(
            curses.newwin(main_window_height, main_window_width, main_y_start, 1)
        )
    )
    user_tab = Panel(
        panel.new_panel(
            curses.newwin(main_window_height, main_window_width, main_y_start, 1)
        )
    )
    user_tab().window().box()
    user_tab().window().refresh()

    list_width = percentage(70, main_window_width)
    list_height = main_window_height - 3

    list_window = Window(password_tab().window().derwin(list_height, list_width, 0, 0))
    list_window().box()
    list_window().addstr(
        1, 1, "Description\tUsername\tCategory\tPassword", curses.A_BOLD
    )
    passwords = retrieve_password_information(cursor, user.username)
    i = 2
    for password in passwords:
        list_window().addstr(
            i, 1, f"{password.description}\t{password.username}\t\t\t********"
        )
        i += 1
    list_window().refresh()

    summary_width = main_window_width - list_width - 1
    summary_window = Window(
        password_tab().window().derwin(list_height, summary_width, 0, list_width + 1)
    )
    summary_window().box()
    summary_window().refresh()

    top_window_height = percentage(15, screen_height) - 1
    top_window = Window(
        window().derwin(
            top_window_height,
            screen_width - 2,
            1,
            1,
        )
    )
    top_window().box()

    top_window().addstr(1, 1, "PPWM", curses.A_BOLD | curses.color_pair(5))
    top_window().addstr(" - Python Password Manager")

    tabs = {"Passwords": password_tab, "User": user_tab}

    window().box()
    window().refresh()

    tabbar = Tabbar(top_window, tabs, (top_window_height - 2, 0))
    top_window().refresh()

    i = 2
    while True:
        input: int = window().getch()
        match input:
            case 9:
                tabbar.next_tab()
            case 81 | 113:
                sys.exit(0)


def percentage(percentage: int, whole: int) -> int:
    return int((whole / 100) * percentage)


password_table = """

"""
