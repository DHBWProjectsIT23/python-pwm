import curses
import sqlite3
from typing import Optional

from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.panel import Panel
from src.tui.views.overview.prompt import Prompt


class SearchPrompt(Prompt):
    def __init__(self,
                 parent: Panel,
                 user: User,
                 cursor: sqlite3.Cursor) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Search"

    def run(self) -> Optional[str]:
        self._reset_prompt(self.title)

        self.prompt_window.write_bottom_center_text(
            "- ↩ Confirm - ^E Cancel -", (-1, 0)
        )
        self.prompt_window().addstr(
            6, 2, "Hint: An empty search shows all passwords", curses.A_ITALIC
        )

        self.prompt_window().addstr(2, 2, "Search Term:", curses.A_UNDERLINE)
        search_textbox, _ = self._create_textbox((1, 32), (4, 2))

        curses.curs_set(True)
        try:
            search_textbox.edit(InputValidator.with_exit)
            term = search_textbox.gather().strip()
        except ExitFromTextBoxException:
            self.prompt_window().clear()
            self.prompt_window().refresh()
            return None
        finally:
            curses.curs_set(False)

        self.prompt_window().clear()
        self.prompt_window().refresh()
        return term
