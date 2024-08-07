import curses
import sqlite3
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.tui.input_validator import InputValidator
from src.tui.views.overview.prompt import Prompt
from src.tui.panel import Panel
from src.model.user import User
from typing import Optional


class SearchPrompt(Prompt):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        super().__init__(parent, user, cursor)
        self.title = "Search"

    def run(self) -> Optional[str]:
        self._reset_prompt(self.title)

        self.prompt.writeBottomCenterText("- ↩ Confirm - ^E Cancel -", (-1, 0))
        self.prompt().addstr(
            6, 2, "Hint: An empty search shows all passwords", curses.A_ITALIC
        )

        self.prompt().addstr(2, 2, "Search Term:", curses.A_UNDERLINE)
        search_textbox, _ = self._create_textbox((1, 32), (4, 2))

        curses.curs_set(True)
        try:
            search_textbox.edit(InputValidator.with_exit)
            term = search_textbox.gather().strip()
        except ExitFromTextBoxException:
            self.prompt().clear()
            self.prompt().refresh()
            return None
        finally:
            curses.curs_set(False)

        self.prompt().clear()
        self.prompt().refresh()
        return term
