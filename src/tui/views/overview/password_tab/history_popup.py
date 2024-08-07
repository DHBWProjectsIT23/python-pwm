import curses
from src.model.password_information import PasswordInformation
from src.tui.keys import Keys
from src.tui.views.overview.prompt import Prompt
from src.tui.panel import Panel


class HistoryPopup:
    def __init__(self, parent: Panel, password: PasswordInformation):
        self.password = password
        height = len(self.password.passwords[-10:]) + 7
        self.password.decrypt_passwords()
        width = (
            max(
                (
                    len(password.password.decode())
                    for password in self.password.passwords
                )
            )
            + 10
        )
        self.popup = Prompt.create_prompt_with_padding(parent, (height, width))

    def run(self) -> None:
        self.popup().box()
        self.popup().addstr(
            0, 0, "Last 10 Passwords", curses.A_BOLD | curses.color_pair(3)
        )
        self.popup.writeBottomCenterText("- ESC Dismiss -", (-1, 0))
        self.popup.writeBottomCenterText(
            "Hint: 1 is the latest", (-2, 0), curses.A_ITALIC
        )

        for i, password in enumerate(reversed(self.password.passwords[-10:])):
            self.popup().addstr(i + 2, 2, f"{i + 1}")
            self.popup().addstr(i + 2, 5, password.password.decode())

        self.popup().refresh()

        while True:
            key_input = self.popup().getch()
            if key_input == Keys.ESCAPE:
                self.popup().clear()
                self.popup().refresh()
                break
