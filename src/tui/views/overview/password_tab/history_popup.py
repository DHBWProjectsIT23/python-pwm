"""
Module for displaying a popup that shows the history of recent passwords.

This module provides functionality to display a popup window showing the last 10 passwords
for a given password information object.
"""
import curses

from src.model.password_information import PasswordInformation
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import SimplePrompt


class HistoryPopup(SimplePrompt):
    """
    Class to display a popup with the history of the last 10 passwords.

    This class inherits from `SimplePrompt` and is used to create a popup that shows the most
    recent 10 passwords from the given `PasswordInformation` object. It includes functionality
    to display these passwords and handle user dismissal of the popup.

    Attributes:
        password (PasswordInformation): 
        The password information object whose history is to be displayed.
    """
    def __init__(self, parent: Panel, password: PasswordInformation):
        """
        Initializes the HistoryPopup class.

        Args:
            parent (Panel): The parent panel where the popup will be displayed.
            password (PasswordInformation): 
            The password information object containing the password history.
        """
        self.password = password
        height = len(self.password.passwords[-10:]) + 7
        self.password.decrypt_passwords()
        width = (
            max(
                (
                    len(password.password_bytes.decode())
                    for password in self.password.passwords
                )
            )
            + 10
        )
        super().__init__(parent, (height, width))

    def run(self) -> None:
        """
        Displays the popup and shows the history of the last 10 passwords.

        This method sets up the popup window, displays the title, hint, and the list of the last
        10 passwords. It then enters a loop to wait for user input to dismiss the popup.
        """
        self.popup().box()
        self.popup().addstr(
            0, 0, "Last 10 Passwords", curses.A_BOLD | curses.color_pair(3)
        )
        self.popup.write_bottom_center_text("- ESC Dismiss -", (-1, 0))
        self.popup.write_bottom_center_text(
            "Hint: 1 is the latest", (-2, 0), curses.A_ITALIC
        )

        for i, password in enumerate(reversed(self.password.passwords[-10:])):
            self.popup().addstr(i + 2, 2, f"{i + 1}")
            self.popup().addstr(i + 2, 5, password.password_bytes.decode())

        self.enter_dismiss_loop()
