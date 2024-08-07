import curses
import sqlite3
from typing import Optional

from src.controller.user import (
    validate_unique_user,
)
from src.crypto.hashing import hash_sha256
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.panel import Panel
from src.tui.views.overview.prompt import Prompt


class UpdateUsernamePrompt(Prompt):
    def __init__(self,
                 parent: Panel,
                 cursor: sqlite3.Cursor,
                 user: User) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Update Username"
        self.prompt = self.create_prompt_with_padding(self.parent)

    def run(self) -> Optional[str]:
        self.break_out()
        self._reset_prompt(self.title)

        try:
            if not self._confirm_password():
                # Lock Account
                self.break_out()
                return None
        except ExitFromTextBoxException:
            self.break_out()
            return None

        try:
            username = self._enter_new_username()
        except ExitFromTextBoxException:
            self.break_out()
            return None

        self._reset_prompt(self.title)
        self.prompt.write_centered_text("Username changed",
                                        (-1, 0),
                                        curses.A_BOLD)
        self.prompt.write_bottom_center_text("- ↩ Continue -", (-1, 0))

        self.break_out()
        return username

    def break_out(self) -> None:
        self.prompt().clear()
        self.prompt().refresh()

    def _enter_new_username(self) -> str:
        self._reset_prompt(self.title)
        self.prompt().addstr(2, 2, "New Username:", curses.A_UNDERLINE)
        self.prompt.write_bottom_center_text("- ↩ Confirm - ^E Cancel -",
                                             (-1, 0))
        username_textbox, _ = self._create_textbox((1, 32), (4, 2))

        while True:
            curses.curs_set(True)
            username_textbox.edit(InputValidator.no_spaces_with_exit)
            username = username_textbox.gather().strip()
            curses.curs_set(False)
            if hash_sha256(username.encode()) == self.user.username:
                self._write_error("Username must be different", self.title)
                continue
            if len(username) < 4:
                self._write_error("Username must have 4 or more characters",
                                  self.title)
                continue
            if not validate_unique_user(self.cursor, username):
                self._write_error("Username is already taken", self.title)
                continue

            return username
