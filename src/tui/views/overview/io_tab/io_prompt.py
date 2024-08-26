"""
Module for handling input-output prompts in a terminal user interface.
Includes the IoPrompt class for managing prompts that require user input.
"""
import curses
import sqlite3
from typing import Any

from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt


class IoPrompt(Prompt):
    """
    A prompt for handling input-output operations in a terminal user interface.
    This class manages user interactions through a prompt window, including
    initializing, confirming inputs, and handling dismiss actions.

    Args:
        parent (Panel): The parent Panel object where the prompt will be displayed.
        user (User): The User object representing the current user.
        cursor (sqlite3.Cursor): The SQLite cursor for database operations.
        title (str): The title of the prompt.
    """
    def __init__(
        self, parent: Panel, user: User, cursor: sqlite3.Cursor, title: str
    ) -> None:
        """
        Initializes the IoPrompt with the given parent panel, user, cursor, and title.

        Args:
            parent (Panel): The parent Panel object where the prompt will be displayed.
            user (User): The User object representing the current user.
            cursor (sqlite3.Cursor): The SQLite cursor for database operations.
            title (str): The title of the prompt.
        """
        super().__init__(parent, user, cursor)
        self.title = title

    def _enter_dismiss_loop(self) -> None:
        """
        Enters a loop that waits for the user to press the Enter key to dismiss the prompt.
        Exits the loop and clears the prompt window upon pressing Enter.
        """
        while True:
            input_key = self.prompt_window().getch()
            if input_key == Keys.ENTER:
                break
        self.break_out()

    def initialize(self) -> None:
        """
        Initializes the prompt by resetting and setting up the prompt window with the title.
        Clears the prompt window and refreshes it to prepare for user interaction.
        """
        self.break_out()
        self._reset_prompt(self.title)

    def break_out(self) -> None:
        """
        Clears the prompt window and refreshes it to remove any displayed content.
        """
        self.prompt_window().clear()
        self.prompt_window().refresh()

    def run(self) -> Any:
        """
        Runs the prompt. This is an abstract method intended to be implemented by subclasses
        to define the specific behavior of the prompt. In this base class, it does nothing.
        """
        pass

    def _confirm(self) -> bool:
        """
        Prompts the user to confirm their action by validating their password.
        If confirmation fails or an exception occurs, it breaks out of the prompt.

        Returns:
            bool: True if confirmation is successful, False otherwise.
        """
        try:
            if not self._confirm_password():
                self.break_out()
                return False
        except ExitFromTextBoxException:
            curses.curs_set(False)
            self.break_out()
            return False
        return True
