"""
Class for handling the password deletion prompt in a terminal user interface.
Prompts the user to confirm and delete a specific password.
"""

import curses
import sqlite3

from src.controller.password import delete_password_information
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt


class DeletePasswordPrompt(Prompt):
    """
    Class for the user prompt to delete a password.

    This class displays a prompt where the user is asked to confirm the deletion of a password.
    Once confirmed, the password is removed from the database.
    """

    def __init__(
        self,
        parent: Panel,
        user: User,
        password: PasswordInformation,
        cursor: sqlite3.Cursor,
    ) -> None:
        """
        Initializes the DeletePasswordPrompt class.

        Args:
            parent (Panel): The parent panel for the prompt.
            user (User): The current user.
            password (PasswordInformation): The password information to be deleted.
            cursor (sqlite3.Cursor): The database cursor for database operations.
        """
        super().__init__(parent, user, cursor)
        self.title = "Delete Password"
        self.password = password

    def run(self) -> bool:
        """
        Executes the prompt to delete the password.

        This method displays a prompt asking the user to confirm the deletion of the password.
        If the user confirms, the password is deleted from the database and True is returned.
        If the user cancels, False is returned.

        Returns:
            bool: True if the password was successfully deleted, otherwise False.
        """
        self._reset_prompt(self.title)
        if not self._confirm_password():
            self.break_out()
            return False

        delete_password_information(self.cursor, self.password)

        self._reset_prompt(self.title)
        self.prompt_window.write_centered_text(
            "Password deleted succesfully!", attr=curses.A_BOLD
        )
        self.prompt_window.write_bottom_center_text("- ↩ Continue -", (-1, 0))
        while True:
            input_key = self.prompt_window().getch()
            if input_key == Keys.ENTER:
                self.break_out()
                return True

    def break_out(self) -> None:
        """
        Clears the prompt window and refreshes the display to exit the prompt.
        """
        self.prompt_window().clear()
        self.prompt_window().refresh()
