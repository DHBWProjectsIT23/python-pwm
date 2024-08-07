import curses
from curses import panel

from src.tui.views.overview.tab_interface import TabInterface
from src.tui.window import Window


class Tabbar:
    def __init__(
            self,
            parent: Window,
            tabs: dict[str, TabInterface],
            position: tuple[int, int]
    ) -> None:
        length: int = 0
        for tab_title in tabs:
            length += len(tab_title) + 2
        self.window: Window = Window(
            parent().derwin(1, length, position[0], position[1])
        )
        self.window().refresh()

        self.tabs: list[Tab] = []

        text_position: int = 0
        for tab_title in tabs.keys():
            self.tabs.append(
                Tab(self.window, tab_title, tabs[tab_title], text_position)
            )
            text_position += len(tab_title) + 2

        self.tabs[0].select()
        self.number_of_tabs = len(self.tabs)
        self.selected = 0
        panel.update_panels()
        curses.doupdate()

    def next_tab(self) -> None:
        self.tabs[self.selected].deselect()
        if self.selected + 1 == self.number_of_tabs:
            self.tabs[0].select()
            self.selected = 0
        else:
            self.selected += 1
            self.tabs[self.selected].select()

        self.refresh()

    def refresh(self) -> None:
        panel.update_panels()
        curses.doupdate()
        self.tabs[self.selected].refresh()


class Tab:
    def __init__(
            self,
            parent: Window,
            title: str,
            tab_content: TabInterface,
            position: int
    ) -> None:
        self.title = title
        self.window: Window = Window(parent().derwin(1,
                                                     len(title) + 2,
                                                     0,
                                                     position))
        self.tab_content: TabInterface = tab_content

        self.window.write_centered_text(self.title, attr=curses.A_UNDERLINE)
        self.window().refresh()

    def select(self) -> None:
        self.window.write_centered_text(
            self.title, attr=curses.A_REVERSE | curses.A_UNDERLINE
        )
        self.window().refresh()
        self.tab_content.show()

    def deselect(self) -> None:
        self.window.write_centered_text(self.title, attr=curses.A_UNDERLINE)
        self.window().refresh()
        self.tab_content.hide()

    def refresh(self) -> None:
        self.tab_content.refresh()
