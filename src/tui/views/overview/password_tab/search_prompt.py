"""
Module for handling search prompts in the user interface.
"""
import curses
import sqlite3
from typing import Optional

from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt


class SearchPrompt(Prompt):
    """
    A class for prompting the user to enter a search term for filtering passwords.

    Inherits from the `Prompt` class and displays a prompt window where the user can enter
    a search term. The entered term is used to filter the password list based on the user's input.

    Attributes:
        title (str): The title of the search prompt.
    """
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor) -> None:
        """
        Initializes the SearchPrompt with the given parent panel, user, and database cursor.

        Args:
            parent (Panel): The parent panel where the prompt is displayed.
            user (User): The user whose passwords are being searched.
            cursor (sqlite3.Cursor): The database cursor for executing queries.
        """
        super().__init__(parent, user, cursor)
        self.title = "Search"

    def run(self) -> Optional[str]:
        """
        Displays the search prompt and waits for the user to enter a search term.

        The prompt allows the user to enter a search term and provides hints for input.
        The user can confirm or cancel the input. The method returns the entered search term
        or `None` if the user cancels the prompt.

        Returns:
            Optional[str]: 
            The search term entered by the user, or `None` if the prompt is cancelled.
        """
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
