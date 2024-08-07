import curses
import sqlite3

from src.controller.password import retrieve_password_information
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.import_export.export_data import export_to_json
from src.model.user import User
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.prompt import Prompt


class ExportPopup(Prompt):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Export Passwords"

    def run(self) -> None:
        self.initialize()

        try:
            if not self._confirm_password():
                # Lock Account
                self.prompt_window().clear()
                self.prompt_window().refresh()
                return
        except ExitFromTextBoxException:
            self.prompt_window().clear()
            self.prompt_window().refresh()
            return

        self._reset_prompt(self.title)
        file = export_to_json(retrieve_password_information(self.cursor, self.user))

        self.prompt_window.write_centered_text(
            f'Succesfully exported to "{file}"', (-1, 0), curses.A_BOLD
        )

        self.prompt_window.write_bottom_center_text("- ↩ Continue -", (-1, 0))

        # File?

        while True:
            input_key = self.prompt_window().getch()
            if input_key == Keys.ENTER:
                break

        self.prompt_window().clear()
        self.prompt_window().refresh()

    def initialize(self) -> None:
        self.prompt_window().clear()
        self.prompt_window().refresh()
        self._reset_prompt(self.title)
