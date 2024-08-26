"""
Module for handling password management within a tab in the user interface.
"""
import curses
import sqlite3
from typing import Optional

import requests

from src.controller.password import insert_password_information
from src.controller.password import retrieve_password_information
from src.controller.password import update_password_information
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.keys import Keys
from src.tui.popup import create_centered_popup
from src.tui.views.overview.components.controls_popup import ControlsPrompt
from src.tui.views.overview.components.tab_interface import TabInterface
from src.tui.views.overview.password_tab.add_password_prompt import (
    show_add_password_prompt,
)
from src.tui.views.overview.password_tab.create_password_prompt import (
    PasswordCreationPrompt,
)
from src.tui.views.overview.password_tab.delete_password_prompt import (
    DeletePasswordPrompt,
)
from src.tui.views.overview.password_tab.edit_password_prompt import PasswordEditPrompt
from src.tui.views.overview.password_tab.history_popup import HistoryPopup
from src.tui.views.overview.password_tab.password_list import PasswordList
from src.tui.views.overview.password_tab.search_prompt import SearchPrompt
from src.tui.views.overview.password_tab.show_details import show_details
from src.tui.window import Window

CONTROLS: dict["str", "str"] = {
    "↑↓": "Navigate Passwords",
    "↩": "Show Details",
    "n": "Create new Password",
    "u": "Update Password",
    "e": "Edit Details",
    "d": "Delete Password",
    "r": "Reveal selected Password",
    "R": "Reveal all Passwords",
    "c": "Check if Password has been leaked",
    "C": "Check all Passwords",
    "s": "Search",
    "h": "Display History",
}


class PasswordTab(TabInterface):
    """
    A class representing a tab in the user interface for managing passwords.

    This class handles the display and interaction with a list of passwords, including operations
    such as viewing details, adding, updating, deleting, revealing, and checking passwords. It
    also supports searching and viewing password history.

    Attributes:
        user (User): The user whose passwords are being managed.
        connection (sqlite3.Connection): 
        The database connection for retrieving and updating password data.
        cursor (sqlite3.Cursor): The database cursor for executing queries.
        controls (dict[str, str]): Dictionary of controls and their descriptions.
        list_window (Window): The window where the list of passwords is displayed.
        password_list (PasswordList): The PasswordList object managing the list of passwords.
    """
    def __init__(
        self,
        window_size: tuple[int, int],
        y_start: int,
        user: User,
        connection: sqlite3.Connection,
    ):
        """
        Initializes the PasswordTab with the given window size, 
        starting position, user, and database connection.

        Args:
            window_size (tuple[int, int]): The size of the window for displaying the password list.
            y_start (int): The starting y-coordinate for the tab.
            user (User): The user whose passwords are being managed.
            connection (sqlite3.Connection): 
            The database connection for retrieving and updating password data.
        """
        super().__init__(window_size, y_start, CONTROLS)

        self.user = user
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.controls = CONTROLS

        list_width = window_size[1]

        self.list_window = Window(
            self.tab().derwin(window_size[0] - 3, list_width, 0, 0)
        )
        self.tab().box()

        self.password_list = PasswordList(
            self.list_window, retrieve_password_information(self.cursor, self.user)
        )
        self._init_table_headings()

    def _init_table_headings(self) -> None:
        """
        Initializes the table headings for the password list.
        """
        desc_width, uname_width, pass_width, _ = PasswordList.calculate_columns(
            self.list_window.get_size()[1]
        )
        heading_attr: int = curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE

        self.list_window().addstr(1, 1, "Description/URL", heading_attr)
        self.list_window().addstr(1, desc_width + 1, "Username", heading_attr)
        self.list_window().addstr(
            1, desc_width + uname_width + 1, "Password", heading_attr
        )
        self.list_window().addstr(
            1, desc_width + uname_width + pass_width + 1, "Status", heading_attr
        )
        self.list_window().refresh()

    async def process_input(self, input_key: int) -> None:
        """
        Processes the user input based on the provided key.

        Args:
            input_key (int): The key pressed by the user.
        """
        match input_key:
            case Keys.ENTER:
                await show_details(self.tab, self.password_list.get_selected())
                self.refresh()
            case Keys.DOWN:
                self.password_list.select_next()
            case Keys.UP:
                self.password_list.select_previous()
            case Keys.E | Keys.E_LOWER:
                self._handle_edit_input()
            case Keys.H | Keys.H_LOWER:
                HistoryPopup(self.tab, self.password_list.get_selected()).run()
                self.refresh()
            case Keys.C_LOWER:
                try:
                    await self.password_list.check_selected()
                except requests.exceptions.ConnectionError:
                    self._display_error(
                        "An Error occured while trying to check the Status"
                    )
                    self.refresh()
            case Keys.C:
                try:
                    await self._handle_check_all_input()
                except ExceptionGroup:
                    self._display_error(
                        "An Error occured while trying to check the Status"
                    )
                    self.refresh()

            case Keys.D | Keys.D_LOWER:
                self._handle_delete_password_input()
            case Keys.N | Keys.N_LOWER:
                self._handle_new_input()

            case Keys.U | Keys.U_LOWER:
                self._handle_add_input()
            case Keys.R_LOWER:
                self.password_list.toggle_selected()
            case Keys.R:
                self._handle_reveal_all_input()
            case Keys.S | Keys.S_LOWER:
                self._handle_search_password_input()
            case Keys.QUESTION_MARK:
                ControlsPrompt(self.tab, self.controls).run()
                self.refresh()

    def _handle_add_input(self) -> None:
        """
        Handles the input for adding a new password to the list.

        Prompts the user to enter a new password and updates the 
        password list and database if successful.
        """
        password_information = self.password_list.get_selected()
        new_password = show_add_password_prompt(self.tab, password_information)
        if new_password is not None:
            password_information.add_password(Password(new_password))
            update_password_information(self.cursor, password_information)
            password_information.decrypt_data()
            self.connection.commit()
            self.reload_passwords()

        self.refresh()

    def _handle_new_input(self) -> None:
        """
        Handles the input for creating a new password entry.

        Prompts the user to enter details for a new password and adds 
        it to the password list and database if successful.
        """
        new_password = PasswordCreationPrompt(self.tab, self.user, self.cursor).run()
        if new_password is not None:
            new_password = insert_password_information(self.cursor, new_password)
            self.connection.commit()
            new_password.decrypt_data()
            self.password_list.add_item(new_password)
            self.reload_passwords()

        self.refresh()

    def _handle_edit_input(self) -> None:
        """
        Handles the input for editing the details of an existing password.

        Prompts the user to edit the selected password and updates the 
        password list and database if successful.
        """
        updated_password = PasswordEditPrompt(
            self.tab, self.user, self.password_list.get_selected(), self.cursor
        ).run()
        if updated_password is None:
            self.refresh()
            return

        update_password_information(self.cursor, updated_password)
        self.connection.commit()
        updated_password.decrypt_data()
        self.password_list.refresh_selected()
        self.reload_passwords()

        self.refresh()

    async def _handle_check_all_input(self) -> None:
        """
        Handles the input for checking the status of all passwords.

        Displays a loading message while checking the status of 
        all passwords and updates the password list.
        """
        loading_message = "Loading..."
        loading_popup = create_centered_popup(
            self.list_window, 5, len(loading_message) + 4
        )
        loading_popup().box()
        loading_popup.write_centered_text(loading_message, (0, 0))
        loading_popup().refresh()
        await self.password_list.check_all()

    def _handle_delete_password_input(self) -> None:
        """
        Handles the input for deleting the selected password.

        Prompts the user to confirm deletion and removes the password 
        from the list and database if confirmed.
        """
        password = self.password_list.get_selected()
        deleted = DeletePasswordPrompt(self.tab, self.user, password, self.cursor).run()
        if deleted:
            self.connection.commit()
            self.reload_passwords()
        else:
            self.refresh()

    def _handle_search_password_input(self) -> None:
        """
        Handles the input for searching passwords.

        Prompts the user to enter a search term and filters the password 
        list based on the search term.
        """
        term = SearchPrompt(self.tab, self.user, self.cursor).run()
        if term is None:
            return
        self.reload_passwords(term)
        self.refresh()

    def _handle_reveal_all_input(self) -> None:
        """
        Handles the input for revealing or hiding all passwords.

        Toggles the visibility of all passwords in the list.
        """
        selected = self.password_list.selected
        for item in self.password_list.items:
            item.showing_pass = not item.showing_pass
            item.deselect()
        self.password_list.items[selected].select()
        self.refresh()

    def reload_passwords(self, search_string: Optional[str] = None) -> None:
        """
        Reloads the password list from the database and optionally filters by a search string.

        Args:
            search_string (Optional[str]): An optional search term to filter the password list.
        """
        passwords = retrieve_password_information(self.cursor, self.user)
        if search_string is not None:
            passwords = list(
                filter(
                    PasswordInformation.create_password_filter(search_string), passwords
                )
            )
        self.password_list = PasswordList(self.list_window, passwords)

    def refresh(self) -> None:
        """
        Refreshes the display of the tab and the password list.

        Updates the tab box, controls, and refreshes the password list and selected item.
        """
        self.tab().box()
        self._display_controls()
        self.tab().refresh()
        self.list_window().refresh()
        self.password_list.refresh_selected()
        self.password_list.refresh()
