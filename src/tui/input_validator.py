import curses
import sys

from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.tui.keys import Keys


class InputValidator:
    def __init__(self) -> None:
        self.password_arr: list[str] = []

    def password(self, ch: int) -> int:
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
        return "".join(self.password_arr).strip()

    def reset_password(self) -> None:
        self.password_arr = []

    @staticmethod
    def no_spaces(ch: int) -> int:
        if ch == 12:
            sys.exit(1)
        if ch == 32:
            return 0

        return ch

    @staticmethod
    def no_spaces_with_exit(ch: int) -> int:
        if ch == 5:
            raise ExitFromTextBoxException
        if ch == 12:
            sys.exit(1)
        if ch == 32:
            return 0

        return ch
