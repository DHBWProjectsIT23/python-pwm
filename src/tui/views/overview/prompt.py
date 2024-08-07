import curses
import sqlite3
from curses.textpad import Textbox
from typing import Any
from typing import TYPE_CHECKING

from src.controller.user import validate_login_hashed
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.popup import create_centered_popup
from src.tui.window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:

    CursesWindow = Any


class Prompt:
    def __init__(
            self,
            parent: Panel,
            user: User,
            cursor: sqlite3.Cursor,
            size: tuple[int, int] = (10, 57),
    ) -> None:
        self.parent = parent
        self.user = user
        self.cursor = cursor
        self.title = ""
        self.prompt_window = Prompt.create_prompt_with_padding(parent, size)

    def run(self) -> Any:
        raise NotImplementedError("This is an interface")

    def _create_textbox(
            self, size: tuple[int, int], position: tuple[int, int]
    ) -> tuple[Textbox, CursesWindow]:
        textbox_window = self.prompt_window().derwin(*size, *position)
        textbox = Textbox(textbox_window)
        self.prompt_window().refresh()
        return textbox, textbox_window

    def _write_error(self, msg: str, title: str) -> None:
        self.prompt_window().box()
        self.prompt_window().addstr(0,
                                    0,
                                    title,
                                    curses.A_BOLD | curses.color_pair(3))
        self.prompt_window.write_bottom_center_text(msg,
                                                    attr=curses.color_pair(2))
        self.prompt_window().refresh()

    def _reset_prompt(self, title: str) -> None:
        self.prompt_window().clear()
        self.prompt_window().box()
        self.prompt_window().addstr(0,
                                    0,
                                    title,
                                    curses.A_BOLD | curses.color_pair(3))
        self.prompt_window().refresh()

    def _confirm_password(self) -> bool:
        self.prompt_window().addstr(
            2, 2, "Confirm Password to Continue", curses.A_UNDERLINE
        )
        self.prompt_window.write_bottom_center_text(
            "- ↩ Confirm - ^E Cancel -", (-1, 0)
        )
        password_textbox, password_window = self._create_textbox((1, 32),
                                                                 (4, 2))
        validator = InputValidator()

        attempts = 0
        while True:
            if attempts > 3:
                return False

            curses.curs_set(True)
            password_textbox.edit(validator.password_with_exit)
            curses.curs_set(False)
            if not validate_login_hashed(
                    self.cursor,
                    self.user.username,
                    validator.get_password_string()
            ):
                self._write_error("Wrong Password", self.title)
                validator.reset_password()
                password_window.clear()
                password_window.refresh()
                attempts += 1
                continue

            return True

    @staticmethod
    def create_prompt_with_padding(
            parent: Panel, size: tuple[int, int] = (10, 57)
    ) -> Window:
        padding = create_centered_popup(parent, size[0] + 2, size[1] + 2)
        padding().refresh()
        prompt = create_centered_popup(parent, *size)
        prompt().clear()
        return prompt


class SimplePrompt:
    def __init__(self, parent: Panel, size: tuple[int, int]):
        self.popup = Prompt.create_prompt_with_padding(parent, size)

    def break_out(self) -> None:
        self.popup().clear()
        self.popup().refresh()

    def enter_dismiss_loop(self):
        self.popup().refresh()
        while True:
            key_input = self.popup().getch()
            if key_input == Keys.ESCAPE:
                self.break_out()
                break
