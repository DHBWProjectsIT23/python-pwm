import curses

from src.tui.panel import Panel
from src.tui.util import generate_control_str

INTERFACE_MSG = "This is an Interface"


class TabInterface:
    def __init__(
        self, window_size: tuple[int, int], y_start: int, controls: dict[str, str]
    ) -> None:
        self.tab = Panel(
            curses.panel.new_panel(
                curses.newwin(window_size[0], window_size[1], y_start, 1)
            )
        )
        self.controls = controls

    async def process_input(self, input_key: int) -> None:
        raise NotImplementedError(INTERFACE_MSG)

    def refresh(self) -> None:
        raise NotImplementedError(INTERFACE_MSG)

    def show(self) -> None:
        self.tab.show()

    def hide(self) -> None:
        self.tab.hide()

    def _display_controls(self) -> None:
        controls_str = generate_control_str(self.controls)
        try:
            self.tab.write_bottom_center_text(controls_str, (-1, 0))
        except ValueError:
            self.tab.write_bottom_center_text("- ? Show Keybinds -", (-1, 0))
        finally:
            self.tab().refresh()
