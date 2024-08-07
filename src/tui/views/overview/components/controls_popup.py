import curses

from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import SimplePrompt


class ControlsPrompt(SimplePrompt):
    def __init__(self, parent: Panel, controls: dict[str, str]):
        self.controls = controls
        height = len(controls) + 5
        width = max((len(f"{key} {value}") for key, value in
                     self.controls.items())) + 5
        super().__init__(parent, (height, width))

        self.value_inset = max(len(key) for key in self.controls.keys()) + 3

    def run(self) -> None:
        self.popup().box()
        self.popup().addstr(0,
                            0,
                            "Controls",
                            curses.A_BOLD | curses.color_pair(3))
        self.popup.write_bottom_center_text("- ESC Dismiss -")

        for i, (key, value) in enumerate(self.controls.items()):
            self.popup().addstr(i + 2, 2, key)
            self.popup().addstr(i + 2, self.value_inset, value)

        self.enter_dismiss_loop()
