import curses
import sqlite3

from src.controller.password import delete_password_information
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt


class DeletePasswordPrompt(Prompt):
    def __init__(
        self,
        parent: Panel,
        user: User,
        password: PasswordInformation,
        cursor: sqlite3.Cursor,
    ) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Delete Password"
        self.password = password

    def run(self) -> bool:
        self._reset_prompt(self.title)
        if not self._confirm_password():
            self.break_out()
            return False

        delete_password_information(self.cursor, self.password)

        self._reset_prompt(self.title)
        self.prompt_window.write_centered_text(
            "Password deleted succesfully!", attr=curses.A_BOLD
        )
        self.prompt_window.write_bottom_center_text("- ↩ Continue -", (-1, 0))
        while True:
            input_key = self.prompt_window().getch()
            if input_key == Keys.ENTER:
                self.break_out()
                return True

    def break_out(self) -> None:
        self.prompt_window().clear()
        self.prompt_window().refresh()
