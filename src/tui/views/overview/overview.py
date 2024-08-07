import curses
import sqlite3
import sys

from src.model.user import User
from src.tui.keys import Keys
from src.tui.util import generate_control_str
from src.tui.util import percentage_of
from src.tui.views.overview.io_tab.io_tab import IoTab
from src.tui.views.overview.password_tab.password_tab import PasswordTab
from src.tui.views.overview.tab_interface import TabInterface
from src.tui.views.overview.tabbar import Tabbar
from src.tui.views.overview.user_tab.user_tab import UserTab
from src.tui.window import Window

CONTROLS: dict[str, str] = {"⇆": "Change Tab", "q": "Quit"}


async def show_overview(
        window: Window, connection: sqlite3.Connection, user: User
) -> None:
    curses.curs_set(False)
    screen_size = window.get_size()
    y_start = percentage_of(15, screen_size[0])

    window_size = screen_size[0] - y_start - 1, screen_size[1] - 2

    password_tab = PasswordTab(window_size, y_start, user, connection)
    user_tab = UserTab(window_size, y_start, user, connection)
    io_tab = IoTab(window_size, y_start, user, connection)

    tabs = {
        "Passwords": password_tab,
        "User": user_tab,
        "Import/Export": io_tab}

    _, tabbar = init_top_window(window, screen_size, tabs)

    window.write_bottom_center_text(generate_control_str(CONTROLS))

    window().refresh()
    password_tab.refresh()

    # tabbar.next_tab()

    while True:
        input_key: int = window().getch()
        match input_key:
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


def init_top_window(
        parent: Window,
        screen_size: tuple[int, int],
        tabs: dict[str, TabInterface]
) -> tuple[Window, Tabbar]:
    top_window_height = percentage_of(15, screen_size[0]) - 1
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

    top_window().refresh()
    return top_window, tabbar
