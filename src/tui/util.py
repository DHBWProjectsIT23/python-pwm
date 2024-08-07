import curses
from typing import TYPE_CHECKING

from .window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


def init_tui(stdscr: CursesWindow) -> Window:
    """
    Initializes the terminal user interface (TUI) by setting up curses
    environment and returning a Window instance.

    Args:
        stdscr (CursesWindow): The standard curses window object used for
                               initializing the TUI.

    Returns:
        Window: A Window object that represents the initialized TUI window.
    """
    stdscr.clear()
    curses.noecho()
    curses.curs_set(False)
    _init_colors(stdscr)
    return Window(stdscr)


def _init_colors(stdscr: CursesWindow) -> None:
    """
    Initializes color pairs for use in the TUI. Sets up default colors and
    color pairs for various text attributes.

    Args:
        stdscr (CursesWindow): The standard curses window object used for
                               initializing color pairs.
    """
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.clear()


def print_centered_logo(window: Window, offset: tuple[int, int]) -> None:
    """
    Prints a centered ASCII logo and caption on the given Window object.

    Args:
        window (Window): The Window object where the logo and caption will
                         be printed.
        offset (tuple[int, int]): The (y, x) offset for positioning the logo.
    """
    logo: str = (
        """
██████  ██████  ██     ██ ███    ███
██   ██ ██   ██ ██     ██ ████  ████
██████  ██████  ██  █  ██ ██ ████ ██
██      ██      ██ ███ ██ ██  ██  ██
██      ██       ███ ███  ██      ██
 """.strip()
    )
    logo_caption = " Python Password Manager "

    window.write_centered_multiline_text(logo, offset, curses.color_pair(5))
    window.write_centered_text(
        logo_caption, (-5, 0), curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE
    )
    window().refresh()


def percentage_of(percentage: int, whole: int) -> int:
    """
    Calculates the specified percentage of a given whole number.

    Args:
        percentage (int): The percentage to calculate.
        whole (int): The whole number from which the percentage is calculated.

    Returns:
        int: The calculated percentage value.
    """
    return int((whole / 100) * percentage)


def shorten_str(text: str, length: int, substitute: str = "...") -> str:
    """
    Shortens a string to a specified length, appending a substitute string if
    necessary.

    Args:
        text (str): The original string to be shortened.
        length (int): The desired length of the shortened string.
        substitute (str, optional): The string to append if shortening is
                                     necessary. Defaults to '...'.

    Returns:
        str: The shortened string with the substitute appended if needed.
    """
    str_len = length - len(substitute)
    return text[:str_len] + substitute


def pad_with(text: str, length: int, padding: str = " ") -> str:
    """
    Pads a string to a specified length with a given padding character.

    Args:
        text (str): The original string to be padded.
        length (int): The desired length of the padded string.
        padding (str, optional): The character to use for padding. Defaults
                                 to a space character.

    Returns:
        str: The padded string.
    """
    return text + (length - len(text)) * padding


def generate_control_str(controls: dict[str, str]) -> str:
    control_str = ""
    for key, value in controls.items():
        control_str += f"- {key} {value} "

    control_str += "-"

    return control_str
