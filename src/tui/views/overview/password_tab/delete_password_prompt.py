import sys
import curses
import sqlite3
from src.controller.password import (
    PasswordInformation,
    delete_password_information,
    delete_password_information_of_user,
)
from src.controller.user import delete_user
from src.tui.keys import Keys
from src.tui.views.overview.prompt import Prompt
from src.tui.panel import Panel
from src.model.user import User


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
            self.prompt().clear()
            self.prompt().refresh()
            return False

        delete_password_information(self.cursor, self.password)

        self._reset_prompt(self.title)
        self.prompt.writeCenteredText(
            "Password deleted succesfully!", attr=curses.A_BOLD
        )
        self.prompt.writeBottomCenterText("- ↩ Continue -", (-1, 0))
        while True:
            input_key = self.prompt().getch()
            if input_key == Keys.ENTER:
                return True
