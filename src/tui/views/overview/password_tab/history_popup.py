import curses

from src.model.password_information import PasswordInformation
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import SimplePrompt


class HistoryPopup(SimplePrompt):
    def __init__(self, parent: Panel, password: PasswordInformation):
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
