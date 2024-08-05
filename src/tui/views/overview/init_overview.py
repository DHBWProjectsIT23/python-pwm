import curses
from curses import panel
from src.model.password_information import PasswordInformation
from src.tui.views.overview.password_list import PasswordList
from src.tui.window import Window
from src.tui.panel import Panel
from src.tui.views.overview.tabbar import Tabbar
from src.tui.util import percentage_of


def init_password_tab(
    window_size: tuple[int, int], y_start: int
) -> tuple[Panel, Window, Window]:
    password_tab = Panel(
        panel.new_panel(curses.newwin(window_size[0], window_size[1], y_start, 1))
    )

    list_width = percentage_of(70, window_size[1])

    list_window = Window(password_tab().derwin(window_size[0], list_width, 0, 0))
    list_window().box()

    summary_width = window_size[1] - list_width - 1
    summary_window = Window(
        password_tab().derwin(window_size[0], summary_width, 0, list_width + 1)
    )
    summary_window().box()

    summary_window().refresh()
    return password_tab, list_window, summary_window


def init_password_list(
    parent: Window, passwords: list[PasswordInformation]
) -> PasswordList:
    password_list = PasswordList(parent, passwords)
    desc_width, uname_width, pass_width, _ = PasswordList.calculate_columns(
        parent.getSize()[1]
    )
    heading_attr: int = curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE

    parent().addstr(1, 1, "Description/URL", heading_attr)
    parent().addstr(1, desc_width + 1, "Username", heading_attr)
    parent().addstr(1, desc_width + uname_width + 1, "Password", heading_attr)
    parent().addstr(
        1, desc_width + uname_width + pass_width + 1, "Status", heading_attr
    )
    parent().refresh()

    password_list.refresh()

    return password_list


def init_user_tab(window_size: tuple[int, int], y_start: int) -> Panel:
    user_tab = Panel(
        panel.new_panel(curses.newwin(window_size[0], window_size[1], y_start, 1))
    )
    user_tab().box()
    user_tab().refresh()
    return user_tab


def init_io_tab(window_size: tuple[int, int], y_start: int) -> Panel:
    io_tab = Panel(
        panel.new_panel(curses.newwin(window_size[0], window_size[1], y_start, 1))
    )
    io_tab().box()
    io_tab().refresh()
    return io_tab


def init_top_window(
    parent: Window, screen_size: tuple[int, int], tabs: dict[str, Panel]
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
