import curses
import sqlite3

from src.controller.password import retrieve_password_information
from src.import_export.export_data import export_to_json
from src.model.user import User
from src.tui.panel import Panel
from src.tui.views.overview.io_tab.io_prompt import IoPrompt


class ExportPrompt(IoPrompt):
    def __init__(self,
                 parent: Panel,
                 user: User,
                 cursor: sqlite3.Cursor) -> None:
        super().__init__(parent, user, cursor, "Export Passwords")

    def run(self) -> None:
        self.initialize()

        if not self._confirm():
            return

        self._reset_prompt(self.title)
        file = export_to_json(retrieve_password_information(self.cursor,
                                                            self.user))

        self.prompt_window.write_centered_text(
            f'Succesfully exported to "{file}"', (-1, 0), curses.A_BOLD
        )

        self.prompt_window.write_bottom_center_text("- ↩ Continue -", (-1, 0))

        # File?

        self._enter_dismiss_loop()
