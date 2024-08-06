import curses
import sys

from src.tui.keys import Keys

from ..window import Window
from ..util import print_centered_logo
from ..popup import create_centered_popup, create_popup

MENU_WINDOW_SIZE: tuple[int, int] = (7, 27)
MENU_ITEM_SIZE: tuple[int, int] = (1, 25)


def show_start(window: Window) -> int:
    login_str = "  Login  "
    # Length - 8
    register_str = "  Register  "

    print_centered_logo(window, (-9, 0))
    print_controls(window)

    menu_window = create_centered_popup(
        window, MENU_WINDOW_SIZE[0], MENU_WINDOW_SIZE[1]
    )

    login_window = init_menu_option(menu_window, login_str, (2, 1))
    hover_item(login_window, login_str)
    register_window = init_menu_option(menu_window, register_str, (4, 1))

    menu_window().box()
    menu_window().refresh()

    selected_option: int = 1
    while True:
        input: int = window().getch()
        match input:
            case Keys.UP:
                hover_item(login_window, login_str)
                unhover_item(register_window, register_str)
                selected_option = 1
            case Keys.DOWN:
                unhover_item(login_window, login_str)
                hover_item(register_window, register_str)
                selected_option = 2
            case Keys.ENTER:
                return selected_option
            case Keys.Q | Keys.q:
                sys.exit(1)


def init_menu_option(parent: Window, text: str, position: tuple[int, int]) -> Window:
    item_window = create_popup(
        parent, position[0], position[1], MENU_ITEM_SIZE[0], MENU_ITEM_SIZE[1]
    )
    item_window.writeCenteredText(text, (0, 0))
    item_window().refresh()
    return item_window


def hover_item(item_window: Window, item_text: str) -> None:
    item_window.writeCenteredText(item_text, (0, 0), curses.A_REVERSE)
    item_window().refresh()


def unhover_item(item_window: Window, item_text: str) -> None:
    item_window.writeCenteredText(item_text, (0, 0))
    item_window().refresh()


def hover_register(register_window: Window, register_str: str) -> None:
    register_window.writeCenteredText(register_str, (0, 0), curses.A_REVERSE)
    register_window().refresh()


def unhover_register(register_window: Window, register_str: str) -> None:
    register_window.writeCenteredText(register_str, (0, 0))
    register_window().refresh()


def print_controls(window: Window) -> None:
    screen_height, screen_width = window.getSize()
    _, width_center = window.getCenter()

    controls_str = "- ↑/↓ Navigate Menu - ↲ Select Option - q Quit -"
    window().addstr(
        screen_height - 2, width_center - (len(controls_str) // 2), controls_str
    )
