from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from curses.panel import _Curses_Panel
    from _curses import _CursesWindow

    CursesPanel = _Curses_Panel
    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesPanel = Any
    CursesWindow = Any


class Panel:
    def __init__(self, panel: CursesPanel) -> None:
        """
        Initialize the Panel with a curses panel object.

        Args:
            panel (CursesPanel): The curses panel object.
        """
        self.panel = panel

    def __call__(self) -> CursesWindow:
        """
        Return the window associated with the panel.

        Returns:
            CursesWindow: The window object associated with the panel.
        """
        return self.panel.window()

    def getSize(self) -> tuple[int, int]:
        """
        Get the size of the panel's window.

        Returns:
            tuple[int, int]: The dimensions of the window (height, width).
        """
        return self.panel.window().getmaxyx()

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
