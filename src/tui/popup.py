from .window import Window


def create_centered_popup(
    window: Window, height: int, width: int, offset: tuple[int, int] = (0, 0)
) -> Window:
    screen_height, screen_width = window.getSize()
    y = (screen_height // 2) - (height // 2) + offset[0]
    x = (screen_width // 2) - (width // 2) + offset[1]
    return create_popup(window, y, x, height, width)


def create_popup(window: Window, y: int, x: int, height: int, width: int) -> Window:
    popup_window = window().derwin(height, width, y, x)
    return Window(popup_window)
