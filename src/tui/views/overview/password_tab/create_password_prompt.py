import curses
import sqlite3
from typing import Optional
from src.controller.password import validate_unique_password
from src.crypto.password_util import generate_secure_password
from src.model.password_information import PasswordInformation
from src.model.password import Password
from src.model.user import User
from src.tui.panel import Panel
from src.tui.views.overview.password_tab import add_password_prompt
from src.tui.views.overview.password_tab.show_generate_menu import (
    show_select_generated_prompt,
)
from src.tui.views.overview.prompt import Prompt
from src.tui.window import Window

CONTROL_E = 5
MULTILINE_CTR_STR = "- ^G Continue -"
SINGLELINE_CTR_STR = "- ↩ Continue -"


class PasswordCreator(Prompt):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor):
        super().__init__(parent)
        self.user = user
        self.cursor = cursor
        self.prompt: Window = Window(parent())

    def run(self) -> Optional[PasswordInformation]:
        title = "New Password"
        choice, self.prompt = show_select_generated_prompt(self.parent, title + " 1/1")
        password_str = ""
        if choice == 1:
            password_str = generate_secure_password()
        elif choice == -1:
            return None

        initial_error = ""
        while True:
            description = self._enter_description(initial_error, title=title + " 2/2")
            username = self._enter_username(title=title + " 3/3")

            if validate_unique_password(self.cursor, description, username, self.user):
                break
            initial_error = "Identical combination already exists"

        password = self._enter_password(password_str, title=title + " 4/4")
        categories = self._enter_categories(title=title + " 5/5")
        note = self._enter_note(title=title + " 6/6")

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

    def _enter_description(
        self, initial_error: str = "", initial_description: str = "", *, title: str
    ) -> str:
        self._reset_prompt(title)
        if len(initial_error) > 0:
            self._write_error(initial_error, title)
        self.prompt().addstr(2, 2, "Description:", curses.A_UNDERLINE)
        self.prompt().addstr(4, 2, initial_description)
        self.prompt().addstr(
            6, 2, "Description/Username combination must be unique", curses.A_ITALIC
        )
        self.prompt.writeBottomCenterText(SINGLELINE_CTR_STR, (-1, 0))
        desc_textbox, _ = self._create_textbox((1, 32), (4, 2))
        desc_textbox.do_command(CONTROL_E)
        while True:
            curses.curs_set(True)
            desc_textbox.edit()
            description = desc_textbox.gather().strip()
            curses.curs_set(False)
            if len(description) == 0:
                self._write_error("Description must not be empty", title)
                continue
            return description

    def _enter_username(
        self, initial_username: str = "", *, title: str
    ) -> Optional[str]:
        title = "New Password 3/3"
        self._reset_prompt(title)

        #! Set Username
        self.prompt().addstr(2, 2, "Optional - Username:", curses.A_UNDERLINE)
        self.prompt().addstr(4, 2, initial_username)
        self.prompt().addstr(
            6, 2, "Description/Username combination must be unique", curses.A_ITALIC
        )
        self.prompt.writeBottomCenterText(SINGLELINE_CTR_STR, (-1, 0))
        username_textbox, _ = self._create_textbox((1, 32), (4, 2))
        username_textbox.do_command(CONTROL_E)
        curses.curs_set(True)
        username_textbox.edit()
        curses.curs_set(False)
        username: Optional[str] = username_textbox.gather().strip()
        return username if len(username) > 0 else None

    def _enter_password(self, password: str, *, title: str) -> Password:
        return Password(
            add_password_prompt.show_password_input(self.prompt, None, password, title)
        )

    def _enter_categories(
        self, initial_categories: list[str] = [], *, title: str
    ) -> list[str]:
        title = "New Password 5/5"
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
        self.prompt.writeBottomCenterText(MULTILINE_CTR_STR, (-1, 0))

        category_textbox, category_window = self._create_textbox((2, 32), (3, 2))
        if len(initial_categories) > 0:
            category_window.addstr(0, 0, ", ".join(initial_categories))
        category_textbox.do_command(CONTROL_E)
        while True:
            curses.curs_set(True)
            category_textbox.edit()
            curses.curs_set(False)
            category_text = category_textbox.gather().strip().replace("\n", "")

            # Validate Categories:
            categories: list[str] = category_text.split(",")
            categories = list(
                set([category.lower().strip() for category in categories])
            )
            if len(categories) > 5:
                self._write_error("Please enter a maximum of 5 Categories", title)
                continue

            return categories

    def _enter_note(
        self, initial_note: Optional[str] = None, *, title: str
    ) -> Optional[str]:
        self._reset_prompt("New Password 6/6")
        self.prompt().addstr(
            2, 2, "Optional - Add a Note to your Password:", curses.A_UNDERLINE
        )
        self.prompt().addstr(6, 2, "Linebreaks are ignored!", curses.A_ITALIC)
        self.prompt.writeBottomCenterText(MULTILINE_CTR_STR, (-1, 0))
        note_textbox, note_window = self._create_textbox((3, 32), (3, 2))
        if initial_note is not None:
            note_window.addstr(initial_note)
        curses.curs_set(True)
        note_textbox.edit()
        curses.curs_set(False)
        note = note_textbox.gather().strip().replace("\n", "")
        return note if len(note) > 0 else None
