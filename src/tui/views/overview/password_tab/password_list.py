"""
Module for managing and displaying a list of passwords in a curses-based user interface.

This module includes classes to create and manage a scrollable list of passwords. Each item
in the list represents a password and its associated details. The list supports selection,
scrolling, and password visibility toggling.
"""

from __future__ import annotations

import asyncio
import curses
from typing import TYPE_CHECKING

from src.model.password_information import PasswordInformation
from src.tui.util import pad_with
from src.tui.util import percentage_of
from src.tui.util import shorten_str
from src.tui.window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Pad = _CursesWindow
    CursesWindow = _CursesWindow
else:
    from typing import Any

    Pad = Any
    CursesWindow = Any


class PasswordList:
    """
    A class to manage and display a list of passwords in a curses window.

    This class provides functionality to display a list of passwords in a scrollable format,
    handle selection, and toggle password visibility.

    Attributes:
        parent (Window): The parent window where the password list is displayed.
        passwords (list[PasswordInformation]): The list of password information to display.
        pad (Pad): The curses pad used for displaying the list of passwords.
        position (int): The current scroll position of the pad.
        selected (int): The index of the currently selected item in the list.
        items (list[ListItem]): The list of ListItem objects representing each password item.
    """

    def __init__(self, parent: Window, passwords: list[PasswordInformation]) -> None:
        """
        Initializes the PasswordList with a given parent window and list of passwords.

        Args:
            parent (Window): The parent window where the password list will be displayed.
            passwords (list[PasswordInformation]):
            The list of PasswordInformation objects to display.
        """
        parent_beg = parent().getbegyx()
        self.pad_beg = parent_beg[0] + 3, parent_beg[1] + 1
        self.parent_max = parent().getmaxyx()
        self.pad_end = self.parent_max[0] + 5, self.parent_max[1] - 1

        if len(passwords) > 0:
            pad_height = len(passwords)
        else:
            pad_height = 1
        pad_width = self.pad_end[1] - 1

        self.pad = curses.newpad(pad_height, pad_width)
        self.position = 0
        self.selected = 0

        self.items: list[ListItem] = []

        for i, password in enumerate(passwords):
            self.items.append(
                ListItem(password, i, self.calculate_columns(self.parent_max[1]), self)
            )

        if len(self.items) > 0:
            self.items[0].select()

    def add_item(self, password: PasswordInformation) -> None:
        """
        Adds a new password to the list and updates the display.

        Args:
            password (PasswordInformation): The new password to add to the list.
        """
        size = self.pad_end[0] - self.pad_beg[0], self.pad_end[1] - self.pad_beg[1]
        self.pad.resize(size[0] + 50, size[1])
        self.items.append(
            ListItem(
                password,
                len(self.items),
                self.calculate_columns(self.parent_max[1]),
                self,
            )
        )
        self.selected = len(self.items) - 1
        self.position = len(self.items)
        self.scroll_down()
        self.refresh()
        self.refresh_selected()

    def refresh(self) -> None:
        """
        Refreshes the display of the pad to show the current view.
        """
        self.pad.refresh(
            self.position,
            0,
            self.pad_beg[0],
            self.pad_beg[1],
            self.pad_end[0],
            self.pad_end[1],
        )

    def select_next(self) -> None:
        """
        Selects the next item in the list and updates the display.
        """
        if len(self.items) == 0:
            return
        self.items[self.selected].deselect()
        if self.selected >= len(self.items) - 1:
            self.selected = len(self.items) - 1
        else:
            self.selected += 1

        self.items[self.selected].select()

        if self.selected <= len(self.items) - 4:
            if self.selected > self.position + self.pad_end[0] - self.pad_beg[0] - 3:
                self.scroll_down()

        self.refresh()

    def select_previous(self) -> None:
        """
        Selects the previous item in the list and updates the display.
        """
        if len(self.items) == 0:
            return
        self.items[self.selected].deselect()
        if self.selected <= 0:
            self.selected = 0
        else:
            self.selected -= 1

        self.items[self.selected].select()

        if self.selected <= self.position + 2:
            self.scroll_up()
        self.refresh()

    def scroll_down(self) -> None:
        """
        Scrolls the view down by one item and refreshes the display.
        """
        if self.position >= self.pad_end[0] - self.pad_beg[0]:
            self.position = self.pad_end[0] - self.pad_beg[0]
        else:
            self.position += 1
        self.refresh()

    def scroll_up(self) -> None:
        """
        Scrolls the view up by one item and refreshes the display.
        """
        if self.position <= 0:
            self.position = 0
        else:
            self.position -= 1
        self.refresh()

    def toggle_selected(self) -> None:
        """
        Toggles the visibility of the selected password and updates the display.
        """
        selected_item = self.items[self.selected]
        selected_item.showing_pass = not selected_item.showing_pass
        selected_item.select()
        self.refresh()

    def get_selected(self) -> PasswordInformation:
        """
        Returns the PasswordInformation object for the currently selected item.

        Returns:
            PasswordInformation: The selected password information.
        """
        return self.items[self.selected].password

    def refresh_selected(self) -> None:
        """
        Refreshes the display of the currently selected item.
        """
        if len(self.items) > 0:
            self.items[self.selected].select()

    async def check_selected(self) -> None:
        """
        Checks the status of the selected password and updates the display.

        This method is asynchronous and performs a status check for the selected password.
        """
        await self.items[self.selected].display_status()
        self.refresh()

    async def check_all(self) -> None:
        """
        Checks the status of all passwords in the list and updates the display.

        This method is asynchronous and performs a status check for each password in the list.
        """
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(item.display_status()) for item in self.items]
            await asyncio.gather(*tasks)
        self.refresh()

    @staticmethod
    def calculate_columns(parent_max_x: int) -> tuple[int, int, int, int]:
        """
        Calculates column widths based on the maximum width of the parent window.

        Args:
            parent_max_x (int): The maximum width of the parent window.

        Returns:
            tuple[int, int, int, int]:
            The widths of the columns for description, username, password, and status.
        """
        col_1 = percentage_of(35, parent_max_x - 2)
        col_2 = percentage_of(20, parent_max_x - 2)
        col_3 = percentage_of(35, parent_max_x - 2)
        col_4 = percentage_of(10, parent_max_x - 2)
        return col_1, col_2, col_3, col_4


class ListItem:
    """
    A class representing a single item in the password list.

    Each ListItem represents a single password entry and handles the display of its details
    in the list.

    Attributes:
        pad (Pad): The curses pad used for displaying the list of passwords.
        position (int): The position of this item in the pad.
        password (PasswordInformation): The password information associated with this item.
        col_width (tuple[int, int, int, int]): The widths of the columns for displaying details.
        pass_list (PasswordList): The parent PasswordList object managing this item.
        showing_pass (bool): Indicates whether the password is currently visible or masked.
    """

    def __init__(
        self,
        password: PasswordInformation,
        position: int,
        column_width: tuple[int, int, int, int],
        parent_list: PasswordList,
    ) -> None:
        """
        Initializes the ListItem with a given password and its display properties.

        Args:
            password (PasswordInformation): The password information for this item.
            position (int): The position of this item in the pad.
            column_width (tuple[int, int, int, int]):
            The widths of the columns for displaying details.
            parent_list (PasswordList): The parent PasswordList object managing this item.
        """
        self.pad = parent_list.pad
        self.position = position
        self.password = password
        self.col_width = column_width
        self.pass_list = parent_list
        self.showing_pass = False
        self.display_description()
        self.display_username()
        self.display_password()
        self.pad.addstr(
            self.position,
            self.col_width[0] + self.col_width[1] + self.col_width[2] + 1,
            "?",
        )

    def display_description(self, attr: int = 0) -> None:
        """
        Displays the description of the password.

        Args:
            attr (int): Optional curses attributes for styling the text.
        """
        description = self.password.details.description.decode()
        if len(description) > self.col_width[0]:
            description = shorten_str(description, self.col_width[0])
        description = pad_with(description, self.col_width[2])
        self.pad.addstr(self.position, 0, description, attr)

    def display_username(self, attr: int = 0) -> None:
        """
        Displays the username associated with the password.

        Args:
            attr (int): Optional curses attributes for styling the text.
        """
        username_bytes = self.password.details.username
        username = "-"
        if username_bytes is not None:
            username = username_bytes.decode()
        if len(username) > self.col_width[0]:
            username = shorten_str(username, self.col_width[1])
        username = pad_with(username, self.col_width[0])
        self.pad.addstr(self.position, self.col_width[0], username, attr)

    def display_password(self, attr: int = 0) -> None:
        """
        Displays the password (masked or visible based on the state).

        Args:
            attr (int): Optional curses attributes for styling the text.
        """
        password = 10 * "*"
        if self.showing_pass:
            self.password.decrypt_passwords()
            password = self.password.passwords[-1].password_bytes.decode()
            if len(password) > self.col_width[2]:
                password = shorten_str(password, self.col_width[2])

        password = pad_with(password, self.col_width[2])
        self.pad.addstr(
            self.position, self.col_width[0] + self.col_width[1], password, attr
        )

    async def display_status(self) -> None:
        """
        Displays the security status of the password.

        This method is asynchronous and performs a status check to indicate whether the password
        has been compromised or not.
        """

        status_col = self.col_width[0] + self.col_width[1] + self.col_width[2] + 1
        self.pad.addstr(self.position, status_col, "-", curses.color_pair(3))

        occurences = await self.password.check_pwned_status()

        if occurences == 0:
            self.pad.addstr(self.position, status_col, "✓", curses.color_pair(3))
        else:
            self.pad.addstr(
                self.position, status_col, f"⚠ {occurences}", curses.color_pair(2)
            )

    def select(self) -> None:
        """
        Highlights the item to indicate that it is selected.
        """
        self.display_description(curses.A_REVERSE)
        self.display_username(curses.A_REVERSE)
        self.display_password(curses.A_REVERSE)

    def deselect(self) -> None:
        """
        Removes the highlight from the item to indicate that it is not selected.
        """
        self.display_description()
        self.display_username()
        self.display_password()
