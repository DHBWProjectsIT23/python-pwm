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
    def __init__(self, panel: CursesPanel) -> None:
        super().__init__(panel.window())
        self.panel = panel

    def getSize(self) -> tuple[int, int]:
        return self.window.getmaxyx()

    def show(self) -> None:
        self.panel.show()

    def hide(self) -> None:
        self.panel.hide()
