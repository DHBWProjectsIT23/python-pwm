"""
Module for handling the I/O tab functionality in a terminal user interface.
Includes the IoTab class for managing import/export operations and menu controls.
"""
import sqlite3

from src.model.user import User
from src.tui.keys import Keys
from src.tui.views.overview.components.controls_popup import ControlsPrompt
from src.tui.views.overview.components.tab_interface import TabInterface
from src.tui.views.overview.io_tab.export_prompt import ExportPrompt
from src.tui.views.overview.io_tab.import_export_menu import ImportExportMenu
from src.tui.views.overview.io_tab.import_prompt import ImportPrompt

CONTROLS: dict["str", "str"] = {
    "↑↓": "Navigate Menu",
    "↩": "Select Option",
}


class IoTab(TabInterface):
    """
    Manages the import/export tab functionality in the terminal user interface.
    Handles user interactions related to importing and exporting passwords,
    and displays control instructions.

    Args:
        window_size (tuple[int, int]): Size of the window (height, width).
        y_start (int): Vertical start position of the tab.
        user (User): The current User object.
        connection (sqlite3.Connection): SQLite database connection.
    """
    def __init__(
        self,
        window_size: tuple[int, int],
        y_start: int,
        user: User,
        connection: sqlite3.Connection,
    ) -> None:
        """
        Initializes the IoTab with the given parameters and sets up the menu.

        Args:
            window_size (tuple[int, int]): Size of the window (height, width).
            y_start (int): Vertical start position of the tab.
            user (User): The current User object.
            connection (sqlite3.Connection): SQLite database connection.
        """
        super().__init__(window_size, y_start, CONTROLS)
        self.tab().box()
        self.menu = ImportExportMenu(self.tab)
        self.user = user
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.controls = CONTROLS

    async def process_input(self, input_key: int) -> None:
        """
        Processes user input for the IoTab. Handles navigation and selection
        based on the key pressed.

        Args:
            input_key (int): The key code of the user input.
        """
        match input_key:
            case Keys.UP:
                self.menu.up_action()
            case Keys.DOWN:
                self.menu.down_action()
            case Keys.ENTER:
                self._handle_enter_input()
            case Keys.QUESTION_MARK:
                ControlsPrompt(self.tab, self.controls).run()
                self.refresh()

    def _handle_enter_input(self) -> None:
        """
        Handles the Enter key input based on the user's menu choice.
        Triggers import or export operations or raises an error for invalid choices.
        """
        if self.menu.get_choice() == 1:
            imported_passwords = ImportPrompt(self.tab, self.user, self.cursor).run()
            if len(imported_passwords) > 0:
                self.connection.commit()
            else:
                self.connection.rollback()
        elif self.menu.get_choice() == 2:
            ExportPrompt(self.tab, self.user, self.cursor).run()
        else:
            raise ValueError("Invalid Menu Option")

        self.refresh()

    def refresh(self) -> None:
        """
        Refreshes the IoTab by updating the menu and control instructions,
        and then refreshing the tab display.
        """
        self.menu.refresh()
        self._display_controls()
        self.tab().refresh()
