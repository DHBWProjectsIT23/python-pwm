"""
Module for defining and managing tab interfaces in a terminal-based application.
Includes the TabInterface class for handling tab-based views and displaying controls and errors.
"""
import curses

from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.util import generate_control_str
from src.tui.views.overview.components.prompt import Prompt

INTERFACE_MSG = "This is an Interface"


class TabInterface:
    """
    Base class for a tab interface in a terminal-based application. Manages the
    display and interaction of a tab, including showing/hiding the tab and displaying
    controls and error messages.

    Args:
        window_size (tuple[int, int]): The size of the tab window (height, width).
        y_start (int): The starting y-coordinate for the tab window.
        controls (dict[str, str]): A dictionary mapping control keys to their descriptions.
    """
    def __init__(
        self, window_size: tuple[int, int], y_start: int, controls: dict[str, str]
    ) -> None:
        """
        Initializes the TabInterface with the given parameters and creates the tab panel.

        Args:
            window_size (tuple[int, int]): The size of the tab window (height, width).
            y_start (int): The starting y-coordinate for the tab window.
            controls (dict[str, str]): A dictionary mapping control keys to their descriptions.
        """
        self.tab = Panel(
            curses.panel.new_panel(
                curses.newwin(window_size[0], window_size[1], y_start, 1)
            )
        )
        self.controls = controls

    async def process_input(self, input_key: int) -> None:
        """
        Processes user input for the tab. This method should be implemented by subclasses
        to define specific tab behavior.

        Args:
            input_key (int): The key code representing the user input.
        
        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError(INTERFACE_MSG)

    def refresh(self) -> None:
        """
        Refreshes the tab display. This method should be implemented by subclasses
        to update the tab content.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError(INTERFACE_MSG)

    def show(self) -> None:
        """
        Shows the tab by making it visible.
        """
        self.tab.show()

    def hide(self) -> None:
        """
        Hides the tab by making it invisible.
        """
        self.tab.hide()

    def _display_controls(self) -> None:
        """
        Displays the control instructions at the bottom of the tab. If an error occurs
        while displaying controls, a default message is shown instead.
        """
        controls_str = generate_control_str(self.controls)
        try:
            self.tab.write_bottom_center_text(controls_str, (-1, 0))
        except ValueError:
            self.tab.write_bottom_center_text("- ? Show Keybinds -", (-1, 0))
        finally:
            self.tab().refresh()

    def _display_error(self, msg: str) -> None:
        """
        Displays an error message in a centered popup within the tab. The user can
        dismiss the popup by pressing the ESC key.

        Args:
            msg (str): The error message to display.
        """
        length = len(msg)
        popup = Prompt.create_prompt_with_padding(self.tab, (6, length + 4))
        popup().box()
        popup().addstr(0, 0, "Error", curses.A_BOLD | curses.color_pair(2))
        popup.write_bottom_center_text("- ESC Dismiss -", (-1, 0))
        popup.write_centered_text(msg, (-1, 0), curses.A_BOLD)
        popup().refresh()

        while True:
            input_key = popup().getch()
            if input_key == Keys.ESCAPE:
                popup().clear()
                popup().refresh()
                return
