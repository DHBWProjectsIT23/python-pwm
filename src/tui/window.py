from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


class Window:
    def __init__(self, window: CursesWindow) -> None:
        """
        Initializes a Window object with a given curses window.

        Args:
            window (CursesWindow): The curses window object to be wrapped by 
                                   this Window class.
        """
        self.window = window

    def getSize(self) -> tuple[int, int]:
        """
        Retrieves the dimensions (height and width) of the window.

        Returns:
            tuple[int, int]: A tuple containing the height and width of the 
                             window.
        """
        return self.window.getmaxyx()

    def getCenter(self) -> tuple[int, int]:
        """
        Calculates the center coordinates of the window.

        Returns:
            tuple[int, int]: A tuple containing the center y-coordinate and 
                             x-coordinate of the window.
        """
        height, width = self.getSize()
        return (height // 2), (width // 2)

    def writeCenteredText(
        self, text: str, offset: tuple[int, int] = (0, 0), attr: int = 0
    ) -> None:
        """
        Writes a string of text centered in the window with an optional offset 
        and attribute.

        Args:
            text (str): The text to be written to the window.
            offset (tuple[int, int], optional): The y and x offset from the 
                                                 center where the text will be 
                                                 placed. Defaults to (0, 0).
            attr (int, optional): The attribute (e.g., color or bold) for the 
                                  text. Defaults to 0.

        Raises:
            ValueError: If the text length exceeds the width of the window.
        """
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
        """
        Writes a string of text centered horizontally at the bottom of the 
        window with an optional offset and attribute.

        Args:
            text (str): The text to be written to the window.
            offset (tuple[int, int], optional): The y and x offset from the 
                                                 bottom center where the text 
                                                 will be placed. Defaults to 
                                                 (0, 0).
            attr (int, optional): The attribute (e.g., color or bold) for the 
                                  text. Defaults to 0.
        """
        bottom_line = (self.getSize()[0] // 2) - 1
        self.writeCenteredText(text, (bottom_line + offset[0], offset[1]), attr)

    def writeCenteredMultilineText(
        self, text: str, offset: tuple[int, int] = (0, 0), attr: int = 0
    ) -> None:
        """
        Writes multiline text centered in the window with an optional offset 
        and attribute.

        Args:
            text (str): The multiline text to be written to the window.
            offset (tuple[int, int], optional): The y and x offset from the 
                                                 center where the text will be 
                                                 placed. Defaults to (0, 0).
            attr (int, optional): The attribute (e.g., color or bold) for the 
                                  text. Defaults to 0.

        Raises:
            ValueError: If the text height or width exceeds the dimensions of 
                        the window.
        """
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
        """
        Allows the Window object to be called as a function to retrieve the 
        underlying curses window.

        Returns:
            CursesWindow: The curses window object wrapped by this Window class.
        """
        return self.window
