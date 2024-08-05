from .panel import Panel
from .window import Window


def create_centered_popup(
    parent: Window | Panel, height: int, width: int, offset: tuple[int, int] = (0, 0)
) -> Window:
    screen_height, screen_width = parent.getSize()
    y = (screen_height // 2) - (height // 2) + offset[0]
    x = (screen_width // 2) - (width // 2) + offset[1]
    return create_popup(parent, y, x, height, width)


def create_popup(
    window: Window | Panel, y: int, x: int, height: int, width: int
) -> Window:
    popup_window = window().derwin(height, width, y, x)
    popup_window.clear()
    return Window(popup_window)
