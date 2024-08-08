import curses
import sys

from src.tui.keys import Keys
from src.tui.popup import create_centered_popup
from src.tui.popup import create_popup
from src.tui.util import print_centered_logo
from src.tui.window import Window

MENU_WINDOW_SIZE: tuple[int, int] = (7, 27)
MENU_ITEM_SIZE: tuple[int, int] = (1, 25)


def show_start(window: Window) -> int:
    """
    Displays the start menu with options to login or register. Handles user
    input for navigating the menu and selecting an option.

    Args:
        window (Window): The Window object used to display the start menu.

    Returns:
        int: The selected option. Returns 1 for "Login" and 2 for "Register".

    Exits:
        sys.exit(1) if the user presses 'q' or 'Q'.
    """
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
        input_key: int = window().getch()
        match input_key:
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
            case Keys.Q | Keys.Q_LOWER:
                sys.exit(1)


def init_menu_option(parent: Window, text: str, position: tuple[int, int]) -> Window:
    """
    Initializes a menu option by creating a popup window for the option and
    displaying the specified text.

    Args:
        parent (Window): The parent Window object where the menu option will be displayed.
        text (str): The text to be displayed in the menu option.
        position (tuple[int, int]): The position (y, x) where the menu option should be placed.

    Returns:
        Window: A Window object representing the created menu option.
    """
    item_window = create_popup(
        parent, position[0], position[1], MENU_ITEM_SIZE[0], MENU_ITEM_SIZE[1]
    )
    item_window.write_centered_text(text, (0, 0))
    item_window().refresh()
    return item_window


def hover_item(item_window: Window, item_text: str) -> None:
    """
    Highlights a menu item by setting its text attribute to reversed colors.

    Args:
        item_window (Window): The Window object representing the menu item to be highlighted.
        item_text (str): The text to be displayed for the highlighted menu item.
    """
    item_window.write_centered_text(item_text, (0, 0), curses.A_REVERSE)
    item_window().refresh()


def unhover_item(item_window: Window, item_text: str) -> None:
    """
    Removes the highlight from a menu item by resetting its text attribute.

    Args:
        item_window (Window): The Window object representing the menu item to be unhighlighted.
        item_text (str): The text to be displayed for the unhighlighted menu item.
    """
    item_window.write_centered_text(item_text, (0, 0))
    item_window().refresh()


def hover_register(register_window: Window, register_str: str) -> None:
    """
    Highlights the "Register" menu item by setting its text attribute to reversed colors.

    Args:
        register_window (Window): The Window object representing the register menu item.
        register_str (str): The text to be displayed for the highlighted register menu item.
    """
    register_window.write_centered_text(register_str, (0, 0), curses.A_REVERSE)
    register_window().refresh()


def unhover_register(register_window: Window, register_str: str) -> None:
    """
    Removes the highlight from the "Register" menu item by resetting its text attribute.

    Args:
        register_window (Window): The Window object representing the register menu item.
        register_str (str): The text to be displayed for the unhighlighted register menu item.
    """
    register_window.write_centered_text(register_str, (0, 0))
    register_window().refresh()


def print_controls(window: Window) -> None:
    """
    Prints the control instructions at the bottom of the window.

    Args:
        window (Window): The Window object where the control instructions will be displayed.
    """
    screen_height, _ = window.get_size()
    _, width_center = window.get_center()

    controls_str = "- ↑/↓ Navigate Menu - ↲ Select Option - q Quit -"
    window().addstr(
        screen_height - 2, width_center - (len(controls_str) // 2), controls_str
    )
