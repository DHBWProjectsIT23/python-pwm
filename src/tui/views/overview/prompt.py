import curses
from src.tui.panel import Panel
from src.tui.popup import create_centered_popup
from src.tui.window import Window
from curses.textpad import Textbox

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


class Prompt:
    def __init__(self, parent: Panel, size: tuple[int, int] = (10, 57)) -> None:
        self.parent = parent
        self.prompt = Prompt.create_prompt_with_padding(parent, size)

    def run(self) -> Any:
        raise NotImplementedError("This is an interface")

    def _create_textbox(
        self, size: tuple[int, int], position: tuple[int, int]
    ) -> tuple[Textbox, CursesWindow]:
        textbox_window = self.prompt().derwin(*size, *position)
        textbox = Textbox(textbox_window)
        self.prompt().refresh()
        return textbox, textbox_window

    def _write_error(self, msg: str, title: str) -> None:
        self.prompt().box()
        self.prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
        self.prompt.writeBottomCenterText(msg, attr=curses.color_pair(2))
        self.prompt().refresh()

    def _reset_prompt(self, title: str) -> None:
        self.prompt().clear()
        self.prompt().box()
        self.prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
        self.prompt().refresh()

    @staticmethod
    def create_prompt_with_padding(
        parent: Panel, size: tuple[int, int] = (10, 57)
    ) -> Window:
        padding = create_centered_popup(parent, size[0] + 2, size[1] + 2)
        padding().refresh()
        prompt = create_centered_popup(parent, *size)
        prompt().clear()
        return prompt
