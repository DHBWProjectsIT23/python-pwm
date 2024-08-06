import curses
from src.tui.views.overview.tab_interface import TabInterface
from src.tui.window import Window
from src.tui.views.overview.tabbar import Tabbar
from src.tui.util import percentage_of


def init_top_window(
    parent: Window, screen_size: tuple[int, int], tabs: dict[str, TabInterface]
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
