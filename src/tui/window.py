from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


class Window:
    def __init__(self, window: CursesWindow) -> None:
        self.window = window

    def getSize(self) -> tuple[int, int]:
        return self.window.getmaxyx()

    def getCenter(self) -> tuple[int, int]:
        height, width = self.getSize()
        return (height // 2), (width // 2)

    def writeCenteredText(
        self, text: str, offset: tuple[int, int] = (0, 0), attr: int = 0
    ) -> None:
        height, width = self.getSize()
        center_y, center_x = self.getCenter()
        y, x = center_y + offset[0], center_x + offset[1]
        text_length = len(text)
        if text_length > width:
            raise ValueError("Text is too long")

        self.window.addstr(y, (x - (text_length // 2)), text, attr)

    def writeBottomCenterText(
        self, text: str, offset: tuple[int, int] = (0, 0), attr: int = 0
    ) -> None:
        bottom_line = (self.getSize()[0] // 2) - 1
        self.writeCenteredText(text, (bottom_line + offset[0], offset[1]), attr)

    def writeCenteredMultilineText(
        self, text: str, offset: tuple[int, int] = (0, 0), attr: int = 0
    ) -> None:
        height, width = self.getSize()
        center_y, center_x = self.getCenter()
        y, x = center_y + offset[0], center_x + offset[1]
        text_length = max(len(line) for line in text.split("\n"))
        if text_length > width:
            raise ValueError("Text is too long")
        text_height = len(text.split("\n"))
        if text_height > height:
            raise ValueError("Text is too long")
        start_y = y - (text_height // 2)
        start_x = x - (text_length // 2)
        for i, line in enumerate(text.split("\n")):
            self.window.addstr(start_y + i, start_x, line, attr)

    def __call__(self) -> CursesWindow:
        return self.window
