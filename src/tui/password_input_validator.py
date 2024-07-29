import curses


class PasswordInputValidator:
    def __init__(self):
        self.password: list[str] = []

    def __call__(self, ch: int) -> int:
        if ch == 10:
            return 7

        if ch in (curses.KEY_BACKSPACE, curses.KEY_DC):
            self.password.pop()
            return curses.KEY_BACKSPACE

        if ch == 32:
            return 0

        if 32 < ch <= 126:
            self.password.append(chr(ch))
            return 42

        return ch

    def get_password_string(self) -> str:
        return "".join(self.password).strip()

    def reset_password(self) -> None:
        self.password = []
