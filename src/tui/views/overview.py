import curses
from src.tui.window import Window


def show_overview(window: Window):
    window().addstr(10, 10, "Hello Word")
    window().refresh()
    screen_height, screen_width = window.getSize()
    list_y_start = percentage(15, screen_height)
    window().addstr(f"{screen_height} - {list_y_start}")
    list_width = percentage(70, screen_width) - 1
    list_height = screen_height - list_y_start - 2

    list_window = Window(window().derwin(list_height, list_width, list_y_start, 1))

    summary_width = screen_width - list_width - 2
    summary_window = Window(
        window().derwin(list_height, summary_width, list_y_start, list_width + 1)
    )

    top_window_height = percentage(15, screen_height) - 2
    top_window = Window(
        window().derwin(
            top_window_height,
        )
    )

    list_window().box()
    list_window().refresh()
    summary_window().box()
    summary_window().refresh()
    window().box()
    window().refresh()

    window().getch()


def percentage(percentage: int, whole: int) -> int:
    return int((whole / 100) * percentage)
