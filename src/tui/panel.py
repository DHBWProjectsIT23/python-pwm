from typing import TYPE_CHECKING

from src.tui.window import Window

if TYPE_CHECKING:
    from curses.panel import _Curses_Panel
    from _curses import _CursesWindow

    CursesPanel = _Curses_Panel
    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesPanel = Any
    CursesWindow = Any


class Panel(Window):
    """
    Initialize the Panel with a curses panel object.

    This class extends the Window class to provide functionality for managing
    panels in a curses-based application.

    Args:
        panel (CursesPanel): The curses panel object to associate with this Panel.
    """

    def __init__(self, panel: CursesPanel) -> None:
        """
        Initialize the Panel instance with a curses panel object.

        Args:
            panel (CursesPanel): The curses panel object to associate with this Panel.
        """
        super().__init__(panel.window())
        self.panel = panel

    def show(self) -> None:
        """
        Show the panel.
        """
        self.panel.show()

    def hide(self) -> None:
        """
        Hide the panel.
        """
        self.panel.hide()
