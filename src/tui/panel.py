from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from curses.panel import _Curses_Panel

    CursesPanel = _Curses_Panel
else:
    from typing import Any

    CursesPanel = Any


class Panel:
    def __init__(self, panel: CursesPanel) -> None:
        self.panel = panel

    def __call__(self) -> CursesPanel:
        return self.panel
