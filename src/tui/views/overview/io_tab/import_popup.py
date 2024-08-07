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
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.prompt import Prompt


class ImportPopup(Prompt):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Import Passwords"

    def run(self) -> list[PasswordInformation]:
        self.initialize()

        try:
            if not self._confirm_password():
                # Lock Account
                self.prompt_window().clear()
                self.prompt_window().refresh()
                return []
        except ExitFromTextBoxException:
            curses.curs_set(False)
            self.prompt_window().clear()
            self.prompt_window().refresh()
            return []

        try:
            file = self._enter_target_file()
        except ExitFromTextBoxException:
            curses.curs_set(False)
            self.prompt_window().clear()
            self.prompt_window().refresh()
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
                self.cursor, password.description.decode(), username, self.user
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

        while True:
            input_key = self.prompt_window().getch()
            if input_key == Keys.ENTER:
                break

        self.prompt_window().clear()
        self.prompt_window().refresh()
        return passwords

    def initialize(self) -> None:
        self.prompt_window().clear()
        self.prompt_window().refresh()
        self._reset_prompt(self.title)

    def _enter_target_file(self) -> str:
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
