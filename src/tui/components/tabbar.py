import curses
from curses import panel
from ..window import Window
from ..panel import Panel


class Tabbar:
    def __init__(
        self, parent: Window, tabs: dict[str, Panel], position: tuple[int, int]
    ) -> None:
        length: int = 0
        for tab_title in tabs:
            length += len(tab_title) + 2
        self.window: Window = Window(
            parent().derwin(1, length, position[0], position[1])
        )
        self.window().refresh()

        self.tabs: list[Tab] = []

        position: int = 0
        for tab_title in tabs.keys():
            self.tabs.append(Tab(self.window, tab_title, tabs[tab_title], position))
            position += len(tab_title) + 2

        self.tabs[0].select()
        self.number_of_tabs = len(self.tabs)
        self.selected = 0
        panel.update_panels()
        curses.doupdate()

    def next_tab(self):
        self.tabs[self.selected].deselect()
        if self.selected + 1 == self.number_of_tabs:
            self.tabs[0].select()
            self.selected = 0
        else:
            self.selected += 1
            self.tabs[self.selected].select()

        panel.update_panels()
        curses.doupdate()


class Tab:
    def __init__(self, parent: Window, title: str, panel: Panel, position: int) -> None:
        self.title = title
        self.window: Window = Window(parent().derwin(1, len(title) + 2, 0, position))
        self.panel: Panel = panel

        self.window.writeCenteredText(self.title, attr=curses.A_UNDERLINE)
        self.window().refresh()

    def select(self):
        self.window.writeCenteredText(
            self.title, attr=curses.A_REVERSE | curses.A_UNDERLINE
        )
        self.window().refresh()
        self.panel().show()

    def deselect(self):
        self.window.writeCenteredText(self.title, attr=curses.A_UNDERLINE)
        self.window().refresh()
        self.panel().hide()
