import curses
import sqlite3
from typing import Any

from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt


class IoPrompt(Prompt):
    def __init__(
        self, parent: Panel, user: User, cursor: sqlite3.Cursor, title: str
    ) -> None:
        super().__init__(parent, user, cursor)
        self.title = title

    def _enter_dismiss_loop(self) -> None:
        while True:
            input_key = self.prompt_window().getch()
            if input_key == Keys.ENTER:
                break
        self.break_out()

    def initialize(self) -> None:
        self.break_out()
        self._reset_prompt(self.title)

    def break_out(self) -> None:
        self.prompt_window().clear()
        self.prompt_window().refresh()

    def run(self) -> Any:
        pass

    def _confirm(self) -> bool:
        try:
            if not self._confirm_password():
                self.break_out()
                return False
        except ExitFromTextBoxException:
            curses.curs_set(False)
            self.break_out()
            return False
        return True
