"""
Module for handling the export of passwords to a JSON file. Includes the ExportPrompt
class which extends IoPrompt to manage the export process and user interactions.
"""

import curses
import sqlite3

from src.controller.password import retrieve_password_information
from src.import_export.export_data import export_to_json
from src.model.user import User
from src.tui.panel import Panel
from src.tui.views.overview.io_tab.io_prompt import IoPrompt


class ExportPrompt(IoPrompt):
    """
    A prompt for exporting passwords to a JSON file. Inherits from IoPrompt and provides
    functionality for confirming the export and displaying the result.

    Args:
        parent (Panel): The parent Panel object where the prompt will be displayed.
        user (User): The User object for the current user.
        cursor (sqlite3.Cursor): The database cursor for accessing password data.
    """

    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        """
        Initializes the ExportPrompt with the given parameters and sets up the prompt title.

        Args:
            parent (Panel): The parent Panel object where the prompt will be displayed.
            user (User): The User object for the current user.
            cursor (sqlite3.Cursor): The database cursor for accessing password data.
        """
        super().__init__(parent, user, cursor, "Export Passwords")

    def run(self) -> None:
        """
        Executes the export prompt. Initializes the prompt, confirms the export action,
        performs the export to a JSON file, and displays a success message with the file path.

        The method handles user interaction for continuing after the export.
        """
        self.initialize()

        if not self._confirm():
            return

        self._reset_prompt(self.title)
        file = export_to_json(retrieve_password_information(self.cursor, self.user))

        self.prompt_window.write_centered_text(
            f'Succesfully exported to "{file}"', (-1, 0), curses.A_BOLD
        )

        self.prompt_window.write_bottom_center_text("- ↩ Continue -", (-1, 0))

        # File?

        self._enter_dismiss_loop()
