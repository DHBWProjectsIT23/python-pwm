"""
A module for validating and processing user input, particularly in the context of password fields.

This module defines the InputValidator class, which includes methods for handling password input,
processing special keys, and managing text input with options for exiting and ignoring spaces.
"""
import curses
import sys

from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.tui.keys import Keys


class InputValidator:
    """
    A class to validate and process user input, particularly for password fields.

    Attributes:
        password_arr (list[str]): A list to store characters of the current password.
    """

    def __init__(self) -> None:
        """
        Initializes an InputValidator instance with an empty list for password characters.
        """
        self.password_arr: list[str] = []

    def password(self, ch: int) -> int:
        """
        Processes a single character input for password entry.

        Args:
            ch (int): The character code of the input.

        Returns:
            int: The processed character code or a special key code.

        Handles:
            - Enter: Returns the bell code.
            - Backspace: Removes the last character 
            from the password and returns the backspace code.
            - Space: Returns null.
            - Printable characters: Adds the character to the password and returns the star code.
        """
        if ch == Keys.ENTER:
            return Keys.BELL

        if ch == curses.KEY_BACKSPACE:
            if len(self.password_arr) > 0:
                self.password_arr.pop()
            return Keys.BACKSPACE

        if ch == Keys.SPACE:
            return Keys.NULL

        # Printable Range
        if Keys.SPACE < ch < Keys.DELETE:
            self.password_arr.append(chr(ch))
            return Keys.STAR.value

        return ch

    def password_with_exit(self, ch: int) -> int:
        """
        Processes a single character input for password entry with an exit option.

        Args:
            ch (int): The character code of the input.

        Returns:
            int: The processed character code or a special key code.

        Handles:
            - Ctrl+E: Raises an ExitFromTextBoxException.
            - Enter: Returns the bell code.
            - Backspace: Removes the last character from the 
            password and returns the backspace code.
            - Space: Returns null.
            - Printable characters: Adds the character to the password and returns the star code.
        """
        if ch == 5:
            raise ExitFromTextBoxException

        if ch == Keys.ENTER:
            return Keys.BELL

        if ch == curses.KEY_BACKSPACE:
            if len(self.password_arr) > 0:
                self.password_arr.pop()
            return Keys.BACKSPACE

        if ch == Keys.SPACE:
            return Keys.NULL

        # Printable Range
        if Keys.SPACE < ch < Keys.DELETE:
            self.password_arr.append(chr(ch))
            return Keys.STAR.value

        return ch

    def get_password_string(self) -> str:
        """
        Retrieves the current password as a string.

        Returns:
            str: The password string composed of the collected characters.
        """
        return "".join(self.password_arr).strip()

    def reset_password(self) -> None:
        """
        Resets the password to an empty state.
        """
        self.password_arr = []

    @staticmethod
    def no_spaces(ch: int) -> int:
        """"
        Processes input to ignore spaces and handle specific key codes.

        Args:
            ch (int): The character code of the input.

        Returns:
            int: The processed character code or an exit code.

        Handles:
            - Ctrl+L: Exits the program.
            - Space: Returns 0.
        """
        if ch == 12:
            sys.exit(1)
        if ch == 32:
            return 0

        return ch

    @staticmethod
    def no_spaces_with_exit(ch: int) -> int:
        """
        Processes input to ignore spaces and handle specific key codes, with an exit exception.

        Args:
            ch (int): The character code of the input.

        Returns:
            int: The processed character code or special exit code.

        Handles:
            - Ctrl+E: Raises an ExitFromTextBoxException.
            - Ctrl+L: Exits the program.
            - Space: Returns 0.
        """
        if ch == 5:
            raise ExitFromTextBoxException
        if ch == 12:
            sys.exit(1)
        if ch == 32:
            return 0

        return ch

    @staticmethod
    def with_exit(ch: int) -> int:
        """
        Processes input to handle specific exit key codes.

        Args:
            ch (int): The character code of the input.

        Returns:
            int: The processed character code or raises an exit exception.

        Handles:
            - Ctrl+E: Raises an ExitFromTextBoxException.
        """
        if ch == 5:
            raise ExitFromTextBoxException
        return ch
