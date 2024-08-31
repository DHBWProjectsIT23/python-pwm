"""
Module for handling the user deletion process in a terminal user interface.

This module provides the `DeleteUserPrompt` class, which facilitates the deletion of a user account
within a terminal-based application. The prompt guides the user through 
the deletion process by asking 
for password confirmation and then proceeding with the deletion of 
the user account and associated data.
"""

import curses
import sqlite3

from src.controller.password import delete_password_information_of_user
from src.controller.user import delete_user
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt


class DeleteUserPrompt(Prompt):
    """
    Handles the user interface prompt for deleting a user account within the terminal application.

    This class provides a terminal-based interface for confirming and
    executing the deletion of a user account.
    It ensures the user confirms their password before proceeding with the deletion process.

    Attributes:
        title (str): The title of the prompt window, set to "Delete User".
    """

    def __init__(
        self,
        parent: Panel,
        user: User,
        cursor: sqlite3.Cursor,
    ) -> None:
        """
        Initializes the DeleteUserPrompt with the given parent panel, user, and database cursor.

        Args:
            parent (Panel): The parent panel where this prompt will be displayed.
            user (User): The user whose account is to be deleted.
            cursor (sqlite3.Cursor): The database cursor for executing database operations.
        """
        super().__init__(parent, user, cursor)
        self.title = "Delete User"

    def run(self) -> bool:
        """
        Executes the user deletion prompt process.

        This method guides the user through the process of deleting
        their account. It performs the following steps:
        1. Resets the prompt window with the title "Delete User".
        2. Asks the user to confirm their password. If the password is
        incorrect or not confirmed, the method
           clears the prompt window and returns `False`.
        3. Deletes all associated password information for the user and
        then deletes the user account from the database.
        4. Resets the prompt window and displays a success message
        indicating that the user has been deleted.
        5. Waits for the user to press the Enter key before exiting the application.

        Returns:
            bool: Returns `True` if the user was successfully deleted
            and the application is to be exited, `False` otherwise.
        """
        self._reset_prompt(self.title)
        if not self._confirm_password():
            self.prompt_window().clear()
            self.prompt_window().refresh()
            return False

        delete_password_information_of_user(self.cursor, self.user)
        delete_user(self.cursor, self.user)

        self._reset_prompt(self.title)
        self.prompt_window.write_centered_text(
            "User deleted succesfully!", attr=curses.A_BOLD
        )
        self.prompt_window.write_bottom_center_text("- ↩ Exit Application -", (-1, 0))
        while True:
            input_key = self.prompt_window().getch()
            if input_key == Keys.ENTER:
                return True
