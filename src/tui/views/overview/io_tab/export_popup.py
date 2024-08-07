import curses
import sqlite3

from src.controller.user import validate_login, validate_login_hashed
from src.controller.password import retrieve_password_information
from src.crypto.hashing import hash_sha256
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.prompt import Prompt
from src.tui.input_validator import InputValidator
from src.import_export.export_data import export_to_json


class ExportPopup(Prompt):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Export Passwords"

    def run(self) -> None:
        self.prompt().clear()
        self.prompt().refresh()
        self._reset_prompt(self.title)

        try:
            if not self._confirm_password():
                # Lock Account
                self.prompt().clear()
                self.prompt().refresh()
                return
        except ExitFromTextBoxException:
            self.prompt().clear()
            self.prompt().refresh()
            return

        self._reset_prompt(self.title)
        file = export_to_json(retrieve_password_information(self.cursor, self.user))

        self.prompt.writeCenteredText(
            f'Succesfully exported to "{file}"', (-1, 0), curses.A_BOLD
        )

        self.prompt.writeBottomCenterText("- ↩ Continue -", (-1, 0))

        # File?

        while True:
            input_key = self.prompt().getch()
            if input_key == Keys.ENTER:
                break

        self.prompt().clear()
        self.prompt().refresh()
