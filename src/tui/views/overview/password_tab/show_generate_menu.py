"""
Module for displaying a prompt to select between generating a 
secure password or entering a custom one.

This module provides functionality to present a prompt in a terminal-based user interface, allowing
the user to choose between generating a secure password or 
entering their own. The prompt handles user
input and updates the display based on the user's selection.
"""

import curses

from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt
from src.tui.window import Window

SELECT_CONTROL_STR = """
- ↩ Continue - ↑↓ Select Option - ^E Cancel -
""".strip()


def show_select_generated_prompt(parent: Panel, title: str) -> tuple[int, Window]:
    """
    Displays a prompt allowing the user to select between generating a
    secure password or entering their own.

    The prompt is presented with two options: "Generate Secure Password" and "Enter Own Password".
    The user can navigate between the options using the up and down arrow keys. The prompt waits for
    the user to press Enter to confirm their selection or Ctrl+E to cancel.

    Args:
        parent (Panel): The parent panel where the prompt will be displayed.
        title (str): The title to be displayed at the top of the prompt.

    Returns:
        tuple[int, Window]: A tuple containing:
            - An integer representing the user's choice
            (1 for generating a secure password, 2 for entering own).
            - The Window object of the prompt.

    Notes:
        - Up arrow key (65) selects the option to generate a secure password.
        - Down arrow key (66) selects the option to enter a custom password.
        - Ctrl+E key (5) cancels the prompt and returns -1.
    """
    prompt = Prompt.create_prompt_with_padding(parent)
    _select_generate(prompt)
    _deselect_own(prompt)
    prompt.write_bottom_center_text(SELECT_CONTROL_STR, (-1, 0))
    prompt().box()
    prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))

    prompt().refresh()

    choice = 1
    while True:
        input_key = prompt().getch()
        match input_key:
            case 65:
                _select_generate(prompt)
                _deselect_own(prompt)
                prompt().refresh()
                choice = 1
            case 66:
                _deselect_generate(prompt)
                _select_own(prompt)
                prompt().refresh()
                choice = 2
            case 5:
                return -1, prompt
            case Keys.ENTER:
                break

    return choice, prompt


def _select_generate(prompt: Window) -> None:
    """
    Highlights the option to generate a secure password in the prompt.

    Args:
        prompt (Window): The prompt window where the option will be highlighted.
    """
    prompt.write_centered_text(" Generate Secure Password ", (-2, 0), curses.A_REVERSE)


def _select_own(prompt: Window) -> None:
    """
    Highlights the option to enter a custom password in the prompt.

    Args:
        prompt (Window): The prompt window where the option will be highlighted.
    """
    prompt.write_centered_text(" Enter Own Password ", (0, 0), curses.A_REVERSE)


def _deselect_generate(prompt: Window) -> None:
    """
    Removes highlighting from the option to generate a secure password in the prompt.

    Args:
        prompt (Window): The prompt window where the highlighting will be removed.
    """
    prompt.write_centered_text(" Generate Secure Password ", (-2, 0))


def _deselect_own(prompt: Window) -> None:
    """
    Removes highlighting from the option to enter a custom password in the prompt.

    Args:
        prompt (Window): The prompt window where the highlighting will be removed.
    """
    prompt.write_centered_text(" Enter Own Password ", (0, 0))
