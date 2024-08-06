import curses
import sys

from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.tui.keys import Keys


class InputValidator:
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

        If `ch` is Enter, returns the bell code.
        If `ch` is Backspace or Delete, removes the last character from the password.
        If `ch` is a printable character, adds it to the password and returns the star code.
        If `ch` is Space, returns null.
        """
        if ch == Keys.ENTER:
            return Keys.BELL

        if ch in (Keys.BACKSPACE, Keys.DELETE):
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

        If `ch` is Ctrl+E (exit), raises an ExitFromTextBoxException.
        If `ch` is Enter, returns the bell code.
        If `ch` is Backspace or Delete, removes the last character from the password.
        If `ch` is Space, returns null.
        If `ch` is a printable character, adds it to the password and returns the star code.
        """
        if ch == 5:
            raise ExitFromTextBoxException

        if ch == Keys.ENTER:
            return Keys.BELL

        if ch in (Keys.BACKSPACE, Keys.DELETE):
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
        """
        Processes input to ignore spaces and exit on specific key codes.

        Args:
            ch (int): The character code of the input.

        Returns:
            int: The processed character code or exit code.

        If `ch` is Ctrl+L (exit), exits the program.
        If `ch` is Space, returns 0.
        """
        if ch == 12:
            sys.exit(1)
        if ch == 32:
            return 0

        return ch

    @staticmethod
    def no_spaces_with_exit(ch: int) -> int:
        """
        Processes input to ignore spaces and exit on specific key codes, with an exit exception.

        Args:
            ch (int): The character code of the input.

        Returns:
            int: The processed character code or special exit code.

        If `ch` is Ctrl+E (exit), raises an ExitFromTextBoxException.
        If `ch` is Ctrl+L (exit), exits the program.
        If `ch` is Space, returns 0.
        """
        if ch == 5:
            raise ExitFromTextBoxException
        if ch == 12:
            sys.exit(1)
        if ch == 32:
            return 0

        return ch
