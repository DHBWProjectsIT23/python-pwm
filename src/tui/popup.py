from .panel import Panel
from .window import Window


def create_centered_popup(
    parent: Window | Panel, height: int, width: int, offset: tuple[int, int] = (0, 0)
) -> Window:
    """
    Create a popup window centered on the parent window or panel with an optional offset.

    Args:
        parent (Window | Panel): The parent window or panel to center the popup on.
        height (int): The height of the popup window.
        width (int): The width of the popup window.
        offset (tuple[int, int], optional): Offset to apply to the centered position (y_offset, x_offset). Defaults to (0, 0).

    Returns:
        Window: A Window object representing the centered popup.
    """
    screen_height, screen_width = parent.getSize()
    y = (screen_height // 2) - (height // 2) + offset[0]
    x = (screen_width // 2) - (width // 2) + offset[1]
    return create_popup(parent, y, x, height, width)


def create_popup(
    window: Window | Panel, y: int, x: int, height: int, width: int
) -> Window:
    """
    Create a popup window at a specified location within the parent window or panel.

    Args:
        window (Window | Panel): The parent window or panel to create the popup in.
        y (int): The y-coordinate (row) of the top-left corner of the popup window.
        x (int): The x-coordinate (column) of the top-left corner of the popup window.
        height (int): The height of the popup window.
        width (int): The width of the popup window.

    Returns:
        Window: A Window object representing the created popup.
    """
    popup_window = window().derwin(height, width, y, x)
    popup_window.clear()
    return Window(popup_window)
