import curses
import sqlite3
from typing import Optional

from src.controller.password import validate_unique_password
from src.crypto.password_util import generate_secure_password
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.panel import Panel
from src.tui.views.overview.password_tab import add_password_prompt
from src.tui.views.overview.password_tab.show_generate_menu import (
    show_select_generated_prompt,
)
from src.tui.views.overview.prompt import Prompt

CONTROL_E = 5
MULTILINE_CTR_STR = "- ^G Continue - ^E Cancel -"
SINGLELINE_CTR_STR = "- ↩ Continue - ^E Cancel -"


class PasswordCreationPrompt(Prompt):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor):
        super().__init__(parent, user, cursor)
        self.prompt = show_select_generated_prompt(self.parent, "New Password")[
            1]
        self.tile = "New Password"

    def run(self) -> Optional[PasswordInformation]:
        choice, self.prompt = show_select_generated_prompt(
            self.parent, self.title + " 1/6"
        )
        password_str = ""
        if choice == 1:
            password_str = generate_secure_password()
        elif choice == -1:
            self.break_out()
            return None

        try:
            initial_error = ""
            while True:
                description = self._enter_description(
                    initial_error, title=self.title + " 2/6"
                )
                username = self._enter_username(title=self.title + " 3/6")

                if validate_unique_password(
                        self.cursor, description, username, self.user
                ):
                    break
                initial_error = "Identical combination already exists"

            password = self._enter_password(password_str,
                                            title=self.title + " 4/6")
            if password is None:
                self.break_out()
                return None
            categories = self._enter_categories(title=self.title + " 5/6")
            note = self._enter_note(title=self.title + " 6/6")

            password_information = PasswordInformation(
                self.user, password, description, username
            )
            if len(categories) > 0:
                password_information.add_categories(categories)
            if note is not None:
                password_information.set_note(note)

            self.prompt().clear()
            self.prompt().refresh()
            return password_information
        except ExitFromTextBoxException:
            self.break_out()
            return None

    def _enter_description(
            self,
            initial_error: str = "",
            initial_description: str = "",
            *,
            title: str
    ) -> str:
        self._reset_prompt(title)
        if len(initial_error) > 0:
            self._write_error(initial_error, title)
        self.prompt().addstr(2, 2, "Description:", curses.A_UNDERLINE)
        self.prompt().addstr(4, 2, initial_description)
        self.prompt().addstr(
            6,
            2,
            "Description/Username combination must be unique",
            curses.A_ITALIC
        )
        self.prompt.write_bottom_center_text(SINGLELINE_CTR_STR, (-1, 0))
        desc_textbox, _ = self._create_textbox((1, 32), (4, 2))
        desc_textbox.do_command(CONTROL_E)
        while True:
            curses.curs_set(True)
            desc_textbox.edit(InputValidator.with_exit)
            description = desc_textbox.gather().strip()
            curses.curs_set(False)
            if len(description) == 0:
                self._write_error("Description must not be empty", title)
                continue
            return description

    def _enter_username(
            self, initial_username: str = "", *, title: str = ""
    ) -> Optional[str]:
        self._reset_prompt(title)

        # ! Set Username
        self.prompt().addstr(2, 2, "Optional - Username:", curses.A_UNDERLINE)
        self.prompt().addstr(4, 2, initial_username)
        self.prompt().addstr(
            6,
            2,
            "Description/Username combination must be unique",
            curses.A_ITALIC
        )
        self.prompt.write_bottom_center_text(SINGLELINE_CTR_STR, (-1, 0))
        username_textbox, _ = self._create_textbox((1, 32), (4, 2))
        username_textbox.do_command(CONTROL_E)
        curses.curs_set(True)
        username_textbox.edit(InputValidator.no_spaces_with_exit)
        curses.curs_set(False)
        username = username_textbox.gather().strip()
        return username if len(username) > 0 else None

    def _enter_password(self, password: str, *, title: str) -> Optional[
        Password]:
        password_str = add_password_prompt.show_password_input(
            self.prompt, None, password, title
        )
        if password_str is None:
            return None

        return Password(password_str)

    def _enter_categories(
            self,
            initial_categories: Optional[list[str]] = None,
            *,
            title: str = ""
    ) -> list[str]:
        if initial_categories is None:
            initial_categories = []
        self._reset_prompt(title)
        self.prompt().addstr(
            2, 2, "Optional - Add up to 5 Categories:", curses.A_UNDERLINE
        )
        self.prompt().addstr(
            5, 2, "Categories should be seperated by a comma", curses.A_ITALIC
        )
        self.prompt().addstr(
            6, 2, 'Example: "Category1, Category2, ... "', curses.A_ITALIC
        )
        self.prompt.write_bottom_center_text(MULTILINE_CTR_STR, (-1, 0))

        category_textbox, category_window = self._create_textbox((2, 32),
                                                                 (3, 2))
        if len(initial_categories) > 0:
            category_window.addstr(0, 0, ", ".join(initial_categories))
        category_textbox.do_command(CONTROL_E)
        while True:
            curses.curs_set(True)
            category_textbox.edit(InputValidator.with_exit)
            curses.curs_set(False)
            category_text = category_textbox.gather().strip().replace("\n", "")

            # Validate Categories:
            categories: list[str] = category_text.split(",")
            categories = list({category.lower().strip() for category in
                               categories})
            if len(categories) > 5:
                self._write_error("Please enter a maximum of 5 Categories",
                                  title)
                continue

            return categories

    def _enter_note(
            self, initial_note: Optional[str] = None, *, title: str
    ) -> Optional[str]:
        self._reset_prompt(title)
        self.prompt().addstr(
            2, 2, "Optional - Add a Note to your Password:", curses.A_UNDERLINE
        )
        self.prompt().addstr(6, 2, "Linebreaks are ignored!", curses.A_ITALIC)
        self.prompt.write_bottom_center_text(MULTILINE_CTR_STR, (-1, 0))
        note_textbox, note_window = self._create_textbox((3, 32), (3, 2))
        if initial_note is not None:
            note_window.addstr(initial_note)
        curses.curs_set(True)
        note_textbox.edit(InputValidator.with_exit)
        curses.curs_set(False)
        note = note_textbox.gather().strip().replace("\n", "")
        return note if len(note) > 0 else None

    def break_out(self) -> None:
        curses.curs_set(False)
        self.prompt().clear()
        self.prompt().refresh()
