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
        self.panel = panel

    def __call__(self) -> CursesWindow:
        return self.panel.window()

    def getSize(self) -> tuple[int, int]:
        return self.panel.window().getmaxyx()

    def show(self) -> None:
        self.panel.show()

    def hide(self) -> None:
        self.panel.hide()
