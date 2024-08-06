import curses
from src.tui.panel import Panel
from src.tui.views.overview.tab_interface import TabInterface
from src.model.user import User


class UserTab(TabInterface):
    def __init__(self, window_size: tuple[int, int], y_start: int, user: User):
        self.tab = Panel(
            curses.panel.new_panel(
                curses.newwin(window_size[0], window_size[1], y_start, 1)
            )
        )
        self.tab().box()
        addstr = self.tab().addstr

        addstr(2, 2, "Username:")

        self.tab().refresh()

    async def process_input(self, input_key: int):
        pass

    def show(self):
        self.tab.show()

    def hide(self):
        self.tab.hide()

    def refresh(self):
        pass
