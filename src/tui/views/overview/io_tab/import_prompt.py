"""
Module for handling password import functionality in a terminal user interface.
Includes the ImportPrompt class for prompting the user to import passwords from a file.
"""
import curses
import os
import sqlite3

from src.controller.password import insert_password_information
from src.controller.password import validate_unique_password
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.exceptions.import_exception import ImportException
from src.import_export.import_data import import_json
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.panel import Panel
from src.tui.views.overview.io_tab.io_prompt import IoPrompt


class ImportPrompt(IoPrompt):
    """
    A prompt for importing passwords from a file. Provides functionality to
    enter a file path, validate and import passwords, and handle any errors that
    occur during the import process.

    Args:
        parent (Panel): The parent Panel object where the prompt will be displayed.
        user (User): The User object representing the current user.
        cursor (sqlite3.Cursor): The SQLite cursor for database operations.
    """

    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        """
        Initializes the ImportPrompt with the given parent panel, user, and database cursor.

        Args:
            parent (Panel): The parent Panel object where the prompt will be displayed.
            user (User): The User object representing the current user.
            cursor (sqlite3.Cursor): The SQLite cursor for database operations.
        """
        super().__init__(parent, user, cursor, "Import Passwords")

    def run(self) -> list[PasswordInformation]:
        """
        Runs the import prompt, allowing the user to import passwords from a file.

        Returns:
            list[PasswordInformation]: A list of PasswordInformation objects representing 
            the imported passwords. If an error occurs or the user cancels, returns an empty list.
        """
        self.initialize()

        if not self._confirm():
            return []

        try:
            file = self._enter_target_file()
        except ExitFromTextBoxException:
            curses.curs_set(False)
            self.break_out()
            return []

        self._reset_prompt(self.title)
        self.prompt_window.write_bottom_center_text("- ↩ Continue -", (-1, 0))
        passwords: list[PasswordInformation] = []
        try:
            passwords = import_json(file, self.user)
            self.prompt_window.write_centered_text(
                "Importing passwords...", (-1, 0), curses.A_BOLD
            )
        except ImportException as e:
            self.prompt_window.write_centered_text(
                f"Error while importing file: {e.message}",
                (-1, 0),
                curses.A_BOLD | curses.color_pair(2),
            )
        except UnicodeDecodeError:
            self.prompt_window.write_centered_text(
                "Error while reading file",
                (-1, 0),
                curses.A_BOLD | curses.color_pair(2),
            )

        for password in passwords:
            username = (
                password.details.username.decode()
                if password.details.username
                else None
            )
            if not validate_unique_password(
                self.cursor, password.details.description.decode(), username, self.user
            ):
                self.prompt_window.write_centered_text(
                    "File contains passwords that are/would be duplicate",
                    (-1, 0),
                    curses.A_BOLD | curses.color_pair(2),
                )
                passwords = []
                break

            insert_password_information(self.cursor, password)

        if len(passwords) > 0:
            self._reset_prompt(self.title)
            self.prompt_window.write_bottom_center_text("- ↩ Continue -", (-1, 0))
            self.prompt_window.write_centered_text(
                f"Imported {len(passwords)} passwords",
                (-1, 0),
                curses.A_BOLD,
            )

        self._enter_dismiss_loop()
        return passwords

    def _enter_target_file(self) -> str:
        """
        Prompts the user to enter the file path for the passwords to import.

        Returns:
            str: The file path entered by the user.

        Raises:
            ExitFromTextBoxException: If the user exits from the textbox input.
        """
        self._reset_prompt(self.title)
        self.prompt_window().addstr(2, 2, "Enter Filepath:", curses.A_UNDERLINE)
        self.prompt_window().addstr(
            6, 2, "The filepath can be absolute or relative", curses.A_ITALIC
        )
        self.prompt_window.write_bottom_center_text(
            "- ↩ Confirm - ^E Cancel -", (-1, 0)
        )

        file_textbox, _ = self._create_textbox((1, 50), (4, 2))
        while True:
            curses.curs_set(True)
            file_textbox.edit(InputValidator.no_spaces_with_exit)
            curses.curs_set(False)
            file_path = file_textbox.gather().strip()
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path

            self._write_error("File not found", self.title)
            self.prompt_window.write_bottom_center_text(
                "- ↩ Confirm - ^E Cancel -", (-1, 0)
            )
