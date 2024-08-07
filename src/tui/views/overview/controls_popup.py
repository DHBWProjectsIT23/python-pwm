import curses
from src.tui.keys import Keys
from src.tui.views.overview.prompt import Prompt
from src.tui.panel import Panel


class ControlsPopup:
    def __init__(self, parent: Panel, controls: dict[str, str]):
        self.controls = controls

        height = len(controls) + 5
        width = max((len(f"{key} {value}") for key, value in self.controls.items())) + 5
        self.value_inset = max(len(key) for key in self.controls.keys()) + 3

        self.popup = Prompt.create_prompt_with_padding(parent, (height, width))

    def run(self) -> None:
        self.popup().box()
        self.popup().addstr(0, 0, "Controls", curses.A_BOLD | curses.color_pair(3))
        self.popup.writeBottomCenterText("- ESC Dismiss -")

        for i, (key, value) in enumerate(self.controls.items()):
            self.popup().addstr(i + 2, 2, key)
            self.popup().addstr(i + 2, self.value_inset, value)

        self.popup().refresh()

        while True:
            key_input = self.popup().getch()
            if key_input == Keys.ESCAPE:
                self.popup().clear()
                self.popup().refresh()
                break
