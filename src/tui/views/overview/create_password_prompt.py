import curses
from curses.textpad import Textbox
import sqlite3
from typing import Optional
from src.controller.password import validate_unique_password
from src.crypto.password_util import generate_secure_password
from src.model.password_information import Password, PasswordInformation
from src.model.user import User
from src.tui.panel import Panel
from src.tui.views.overview import add_password_prompt
from src.tui.views.overview.select_generated import show_select_generated_prompt
from src.tui.window import Window

MULTILINE_CTR_STR = "- ^G Continue -"
SINGLELINE_CTR_STR = "- ↩ Continue -"


class PasswordCreator:
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor):
        self.parent = parent
        self.user = user
        self.cursor = cursor
        self.prompt: Optional[Window] = None

    def run(self) -> Optional[PasswordInformation]:
        choice, self.prompt = show_select_generated_prompt(
            self.parent, "New Password 1/1"
        )
        password_str = ""
        if choice == 1:
            password_str = generate_secure_password()
        elif choice == -1:
            return None

        initial_error = ""
        while True:
            description = self._enter_description(initial_error)
            username = self._enter_username()

            if validate_unique_password(self.cursor, description, username, self.user):
                break
            initial_error = "Identical combination already exists"

        password = self._enter_password(password_str)
        categories = self._enter_categories()
        note = self._enter_note()

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

    def _enter_description(self, initial_error: str = "") -> str:
        title = "New Password 2/2"
        self._reset_prompt(title)
        if len(initial_error) > 0:
            self._write_error(initial_error, title)
        self.prompt().addstr(2, 2, "Description:", curses.A_UNDERLINE)
        self.prompt().addstr(
            6, 2, "Description/Username combination must be unique", curses.A_ITALIC
        )
        self.prompt.writeBottomCenterText(SINGLELINE_CTR_STR, (-1, 0))
        desc_textbox = self._create_textbox((1, 32), (4, 2))
        while True:
            curses.curs_set(True)
            desc_textbox.edit()
            description = desc_textbox.gather().strip()
            curses.curs_set(False)
            if len(description) == 0:
                self._write_error("Description must not be empty", title)
                continue
            return description

    def _enter_username(self) -> Optional[str]:
        title = "New Password 3/3"
        self._reset_prompt(title)

        #! Set Username
        self.prompt().addstr(2, 2, "Optional - Username:", curses.A_UNDERLINE)
        self.prompt().addstr(
            6, 2, "Description/Username combination must be unique", curses.A_ITALIC
        )
        self.prompt.writeBottomCenterText(SINGLELINE_CTR_STR, (-1, 0))
        username_textbox = self._create_textbox((1, 32), (4, 2))
        curses.curs_set(True)
        username_textbox.edit()
        curses.curs_set(False)
        username: Optional[str] = username_textbox.gather().strip()
        return username if len(username) > 0 else None

    def _enter_password(self, password: str) -> Password:
        return Password(
            add_password_prompt.show_password_input(
                self.prompt, None, password, "New Password 4/4"
            )
        )

    def _enter_categories(self) -> list[str]:
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

        category_textbox = self._create_textbox((2, 32), (3, 2))
        while True:
            curses.curs_set(True)
            category_textbox.edit()
            curses.curs_set(False)
            category_text = category_textbox.gather().strip()

            # Validate Categories:
            categories: list[str] = category_text.split(",")
            categories = list(
                set([category.lower().strip() for category in categories])
            )
            if len(categories) > 5:
                self._write_error("Please enter a maximum of 5 Categories", title)
                continue

            return categories

    def _enter_note(self) -> Optional[str]:
        self._reset_prompt("New Password 6/6")
        self.prompt().addstr(
            2, 2, "Optional - Add a Note to your Password:", curses.A_UNDERLINE
        )
        self.prompt.writeBottomCenterText(MULTILINE_CTR_STR, (-1, 0))
        note_textbox = self._create_textbox((3, 32), (3, 2))
        curses.curs_set(True)
        note_textbox.edit()
        curses.curs_set(False)
        note = note_textbox.gather().strip().replace("\n", " ")
        return note if len(note) > 0 else None

    def _create_textbox(
        self, size: tuple[int, int], position: tuple[int, int]
    ) -> Textbox:
        textbox_window = self.prompt().derwin(*size, *position)
        textbox = Textbox(textbox_window)
        self.prompt().refresh()
        return textbox

    def _write_error(self, msg: str, title: str):
        self.prompt().box()
        self.prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
        self.prompt.writeBottomCenterText(msg, attr=curses.color_pair(2))
        self.prompt().refresh()

    def _reset_prompt(self, title: str):
        self.prompt().clear()
        self.prompt().box()
        self.prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
        self.prompt().refresh()
