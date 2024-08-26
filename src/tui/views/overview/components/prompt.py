"""
Module for defining prompt interfaces and handling user interactions in a
terminal-based application. Includes base classes for prompts and simple prompts,
and methods for managing user input and validation.
"""
import curses
import sqlite3
from curses.textpad import Textbox
from typing import Any
from typing import TYPE_CHECKING

from src.controller.user import validate_login_hashed
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.popup import create_centered_popup
from src.tui.window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:

    CursesWindow = Any


class Prompt:
    """
    Base class for creating prompts in the terminal. Manages the display and
    interaction with a prompt window, including handling user input and validation.

    Args:
        parent (Panel): The parent Panel object where the prompt will be displayed.
        user (User): The User object for authentication and user-related operations.
        cursor (sqlite3.Cursor): The database cursor used for querying.
        size (tuple[int, int]): The size of the prompt window (height, width).
    """
    def __init__(
        self,
        parent: Panel,
        user: User,
        cursor: sqlite3.Cursor,
        size: tuple[int, int] = (10, 57),
    ) -> None:
        """
        Initializes the Prompt with the given parameters and creates the prompt window.

        Args:
            parent (Panel): The parent Panel object where the prompt will be displayed.
            user (User): The User object for authentication and user-related operations.
            cursor (sqlite3.Cursor): The database cursor used for querying.
            size (tuple[int, int]): The size of the prompt window (height, width).
        """
        self.parent = parent
        self.user = user
        self.cursor = cursor
        self.title = ""
        self.prompt_window = Prompt.create_prompt_with_padding(parent, size)

    def run(self) -> Any:
        """
        Runs the prompt. This method should be implemented by subclasses to define
        specific prompt behavior.

        Raises:
            NotImplementedError: This is an abstract method and should be implemented
                                  by subclasses.
        """
        raise NotImplementedError("This is an interface")

    def _create_textbox(
        self, size: tuple[int, int], position: tuple[int, int]
    ) -> tuple[Textbox, CursesWindow]:
        """
        Creates a Textbox widget within the prompt window at the specified position.

        Args:
            size (tuple[int, int]): The size of the Textbox (height, width).
            position (tuple[int, int]): The position (y, x) where the Textbox should be placed.

        Returns:
            tuple[Textbox, CursesWindow]: A tuple containing the Textbox widget and its
                                           associated Curses window.
        """
        textbox_window = self.prompt_window().derwin(*size, *position)
        textbox = Textbox(textbox_window)
        self.prompt_window().refresh()
        return textbox, textbox_window

    def _write_error(self, msg: str, title: str) -> None:
        """
        Displays an error message in the prompt window.

        Args:
            msg (str): The error message to display.
            title (str): The title of the prompt window.
        """
        self.prompt_window().box()
        self.prompt_window().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
        self.prompt_window.write_bottom_center_text(msg, attr=curses.color_pair(2))
        self.prompt_window().refresh()

    def _reset_prompt(self, title: str) -> None:
        """
        Resets the prompt window with a new title.

        Args:
            title (str): The new title to display in the prompt window.
        """
        self.prompt_window().clear()
        self.prompt_window().box()
        self.prompt_window().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
        self.prompt_window().refresh()

    def _confirm_password(self) -> bool:
        """
        Prompts the user to confirm their password. 
        Returns True if the password is correct,
        False if the maximum number of attempts is exceeded.

        Returns:
            bool: True if the password is confirmed, False otherwise.
        """
        self.prompt_window().addstr(
            2, 2, "Confirm Password to Continue", curses.A_UNDERLINE
        )
        self.prompt_window.write_bottom_center_text(
            "- ↩ Confirm - ^E Cancel -", (-1, 0)
        )
        password_textbox, password_window = self._create_textbox((1, 32), (4, 2))
        validator = InputValidator()

        attempts = 0
        while True:
            if attempts > 3:
                return False

            curses.curs_set(True)
            password_textbox.edit(validator.password_with_exit)
            curses.curs_set(False)
            if not validate_login_hashed(
                self.cursor, self.user.username, validator.get_password_string()
            ):
                self._write_error("Wrong Password", self.title)
                validator.reset_password()
                password_window.clear()
                password_window.refresh()
                attempts += 1
                continue

            return True

    @staticmethod
    def create_prompt_with_padding(
        parent: Panel, size: tuple[int, int] = (10, 57)
    ) -> Window:
        """
        Creates a prompt window with padding around it.

        Args:
            parent (Panel): The parent Panel object where the prompt will be displayed.
            size (tuple[int, int]): The size of the prompt window (height, width).

        Returns:
            Window: A Window object representing the prompt with padding.
        """
        padding = create_centered_popup(parent, size[0] + 2, size[1] + 2)
        padding().refresh()
        prompt = create_centered_popup(parent, *size)
        prompt().clear()
        return prompt


class SimplePrompt:
    """
    A simple prompt class that displays a prompt window and handles basic user input.
    Inherits from Prompt and provides functionality to dismiss the prompt with a key press.

    Args:
        parent (Panel): The parent Panel object where the prompt will be displayed.
        size (tuple[int, int]): The size of the prompt window (height, width).
    """
    def __init__(self, parent: Panel, size: tuple[int, int]) -> None:
        """
        Initializes the SimplePrompt with the given parameters and creates the prompt window.

        Args:
            parent (Panel): The parent Panel object where the prompt will be displayed.
            size (tuple[int, int]): The size of the prompt window (height, width).
        """
        self.popup = Prompt.create_prompt_with_padding(parent, size)

    def break_out(self) -> None:
        """
        Clears and refreshes the prompt window to exit the prompt.
        """
        self.popup().clear()
        self.popup().refresh()

    def enter_dismiss_loop(self) -> None:
        """
        Enters a loop that waits for user input to dismiss the prompt. The prompt
        is dismissed when the ESC key is pressed.
        """
        self.popup().refresh()
        while True:
            key_input = self.popup().getch()
            if key_input == Keys.ESCAPE:
                self.break_out()
                break
