"""
Module for displaying a prompt with control instructions in a terminal-based
user interface. The `ControlsPrompt` class inherits from `SimplePrompt` and
is used to display key-value pairs representing control instructions.
"""
import curses

from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import SimplePrompt


class ControlsPrompt(SimplePrompt):
    """
    Displays a prompt with control instructions, showing a list of key-value
    pairs that describe the controls available in the application.

    Inherits:
        SimplePrompt: Base class for creating and managing prompts.

    Args:
        parent (Panel): The parent Panel object where the prompt will be displayed.
        controls (dict[str, str]): A dictionary where keys are control keys and values
                                   are descriptions of those controls.
    """
    def __init__(self, parent: Panel, controls: dict[str, str]):
        """
        Initializes the ControlsPrompt with the parent panel and control instructions.

        Args:
            parent (Panel): The parent Panel object where the prompt will be displayed.
            controls (dict[str, str]): A dictionary where keys are control keys and values
                                       are descriptions of those controls.
        """
        self.controls = controls
        height = len(controls) + 5
        width = max((len(f"{key} {value}") for key, value in self.controls.items())) + 5
        super().__init__(parent, (height, width))

        self.value_inset = max(len(key) for key in self.controls.keys()) + 3

    def run(self) -> None:
        """
        Runs the prompt, displaying the control instructions and handling user input
        to dismiss the prompt.
        """
        self.popup().box()
        self.popup().addstr(0, 0, "Controls", curses.A_BOLD | curses.color_pair(3))
        self.popup.write_bottom_center_text("- ESC Dismiss -")

        for i, (key, value) in enumerate(self.controls.items()):
            self.popup().addstr(i + 2, 2, key)
            self.popup().addstr(i + 2, self.value_inset, value)

        self.enter_dismiss_loop()
