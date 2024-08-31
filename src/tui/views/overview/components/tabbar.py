"""
Module for managing tab bars and individual tabs in a terminal-based application.
Includes the Tabbar class for handling tab navigation and the Tab class for individual tabs.
"""
import curses
from curses import panel

from src.tui.views.overview.components.tab_interface import TabInterface
from src.tui.window import Window


class Tabbar:
    """
    Manages a horizontal bar of tabs in a terminal-based application. Allows for
    navigation between tabs and handles the display and selection of tabs.

    Args:
        parent (Window): The parent Window object where the tab bar will be displayed.
        tabs (dict[str, TabInterface]): A dictionary mapping tab titles 
        to their corresponding TabInterface objects.
        position (tuple[int, int]): The (y, x) position where the tab bar should be placed.
    """
    def __init__(
        self, parent: Window, tabs: dict[str, TabInterface], position: tuple[int, int]
    ) -> None:
        """
        Initializes the Tabbar with the given parameters and creates the tabs.

        Args:
            parent (Window): The parent Window object where the tab bar will be displayed.
            tabs (dict[str, TabInterface]): A dictionary mapping tab 
            titles to their corresponding TabInterface objects.
            position (tuple[int, int]): The (y, x) position where the tab bar should be placed.
        """
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
        """
        Switches to the next tab in the tab bar. 
        Wraps around to the first tab if currently on the last tab.
        """
        self.tabs[self.selected].deselect()
        if self.selected + 1 == self.number_of_tabs:
            self.tabs[0].select()
            self.selected = 0
        else:
            self.selected += 1
            self.tabs[self.selected].select()

        self.refresh()

    def refresh(self) -> None:
        """
        Refreshes the tab bar display and the currently selected tab.
        """
        panel.update_panels()
        curses.doupdate()
        self.tabs[self.selected].refresh()


class Tab:
    """
    Represents an individual tab in a tab bar, including its title and content. Handles
    the display and selection of the tab.

    Args:
        parent (Window): The parent Window object where the tab will be displayed.
        title (str): The title of the tab.
        tab_content (TabInterface): The TabInterface object associated with the tab content.
        position (int): The x-position where the tab should be placed in the tab bar.
    """
    def __init__(
        self, parent: Window, title: str, tab_content: TabInterface, position: int
    ) -> None:
        """
        Initializes the Tab with the given parameters and sets up its display.

        Args:
            parent (Window): The parent Window object where the tab will be displayed.
            title (str): The title of the tab.
            tab_content (TabInterface): The TabInterface object associated with the tab content.
            position (int): The x-position where the tab should be placed in the tab bar.
        """
        self.title = title
        self.window: Window = Window(parent().derwin(1, len(title) + 2, 0, position))
        self.tab_content: TabInterface = tab_content

        self.window.write_centered_text(self.title, attr=curses.A_UNDERLINE)
        self.window().refresh()

    def select(self) -> None:
        """
        Selects the tab by highlighting it and displaying its content.
        """
        self.window.write_centered_text(
            self.title, attr=curses.A_REVERSE | curses.A_UNDERLINE
        )
        self.window().refresh()
        self.tab_content.show()

    def deselect(self) -> None:
        """
        Deselects the tab by removing the highlight and hiding its content.
        """
        self.window.write_centered_text(self.title, attr=curses.A_UNDERLINE)
        self.window().refresh()
        self.tab_content.hide()

    def refresh(self) -> None:
        """
        Refreshes the display of the tab content.
        """
        self.tab_content.refresh()
