import curses
import os
import sqlite3
from typing import Optional

from src.controller.user import validate_login, validate_login_hashed
from src.controller.password import (
    insert_password_information,
    retrieve_password_information,
    validate_unique_password,
)
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.exceptions.import_exception import ImportException
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.password_tab.password_list import PasswordList
from src.tui.views.overview.prompt import Prompt
from src.tui.input_validator import InputValidator
from src.import_export.import_data import import_json


class ImportPopup(Prompt):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        super().__init__(parent)
        self.user = user
        self.cursor = cursor
        self.title = "Import Passwords"

    def run(self) -> list[PasswordInformation]:
        self.prompt = self.create_prompt_with_padding(self.parent)
        self.prompt().clear()
        self.prompt().refresh()
        self._reset_prompt(self.title)

        try:
            if not self._confirm_password():
                # Lock Account
                self.prompt().clear()
                self.prompt().refresh()
                return None
        except ExitFromTextBoxException:
            self.prompt().clear()
            self.prompt().refresh()
            return None

        # File?
        file = ""
        try:
            file = self._enter_target_file()
        except ExitFromTextBoxException:
            self.prompt().clear()
            self.prompt().refresh()
            return None

        self._reset_prompt(self.title)
        self.prompt.writeBottomCenterText("- ↩ Continue -", (-1, 0))
        passwords: list[PasswordInformation] = []
        try:
            passwords = import_json(file, self.user)
            self.prompt.writeCenteredText(
                "Importing passwords...", (-1, 0), curses.A_BOLD
            )
        except ImportException as e:
            self.prompt.writeCenteredText(
                f"Error while importing file: {e.message}",
                (-1, 0),
                curses.A_BOLD | curses.color_pair(2),
            )
        except UnicodeDecodeError:
            self.prompt.writeCenteredText(
                "Error while reading file",
                (-1, 0),
                curses.A_BOLD | curses.color_pair(2),
            )

        for password in passwords:
            username = password.username.decode() if password.username else None
            if not validate_unique_password(
                self.cursor, password.description.decode(), username, self.user
            ):
                self.prompt.writeCenteredText(
                    "File contains passwords that are/would be duplicate",
                    (-1, 0),
                    curses.A_BOLD | curses.color_pair(2),
                )
                passwords = []
                break

            insert_password_information(self.cursor, password)

        if len(passwords) > 0:
            self._reset_prompt(self.title)
            self.prompt.writeBottomCenterText("- ↩ Continue -", (-1, 0))
            self.prompt.writeCenteredText(
                f"Imported {len(passwords)} passwords",
                (-1, 0),
                curses.A_BOLD,
            )

        while True:
            input_key = self.prompt().getch()
            if input_key == Keys.ENTER:
                break

        self.prompt().clear()
        self.prompt().refresh()
        return passwords

    def _confirm_password(self) -> bool:
        self.prompt().addstr(
            2, 2, "Confirm Masterpassword to Import:", curses.A_UNDERLINE
        )
        self.prompt.writeBottomCenterText("- ↩ Confirm - ^E Cancel -", (-1, 0))
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

    def _enter_target_file(self) -> str:
        self._reset_prompt(self.title)
        self.prompt().addstr(2, 2, "Enter Filepath:", curses.A_UNDERLINE)
        self.prompt().addstr(
            6, 2, "The filepath can be absolute or relative", curses.A_ITALIC
        )
        self.prompt.writeBottomCenterText("- ↩ Confirm - ^E Cancel -", (-1, 0))

        file_textbox, _ = self._create_textbox((1, 50), (4, 2))
        while True:
            curses.curs_set(True)
            file_textbox.edit(InputValidator.no_spaces_with_exit)
            curses.curs_set(False)
            file_path = file_textbox.gather().strip()
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path

            self._write_error("File not found", self.title)
        self.prompt.writeBottomCenterText("- ↩ Confirm - ^E Cancel -", (-1, 0))
