import sys
import curses
import sqlite3
from src.controller.password import delete_password_information_of_user
from src.controller.user import delete_user
from src.tui.keys import Keys
from src.tui.views.overview.prompt import Prompt
from src.tui.panel import Panel
from src.model.user import User


class DeleteUserPrompt(Prompt):
    def __init__(
        self,
        parent: Panel,
        user: User,
        cursor: sqlite3.Cursor,
    ) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Delete User"

    def run(self) -> bool:
        self._reset_prompt(self.title)
        if not self._confirm_password():
            self.prompt().clear()
            self.prompt().refresh()
            return False

        delete_password_information_of_user(self.cursor, self.user)
        delete_user(self.cursor, self.user)

        self._reset_prompt(self.title)
        self.prompt.writeCenteredText("User deleted succesfully!", attr=curses.A_BOLD)
        self.prompt.writeBottomCenterText("- ↩ Exit Application -", (-1, 0))
        while True:
            input_key = self.prompt().getch()
            if input_key == Keys.ENTER:
                return True
