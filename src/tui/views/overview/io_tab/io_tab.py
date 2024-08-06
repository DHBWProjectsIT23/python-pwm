import curses
import sqlite3
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.model.user import User
from src.tui.views.overview.io_tab.export_popup import ExportPopup
from src.tui.views.overview.io_tab.import_export_menu import ImportExportMenu
from src.tui.views.overview.io_tab.import_popup import ImportPopup
from src.tui.views.overview.tab_interface import TabInterface


class IoTab(TabInterface):
    def __init__(
        self,
        window_size: tuple[int, int],
        y_start: int,
        user: User,
        connection: sqlite3.Connection,
    ) -> None:
        self.tab = Panel(
            curses.panel.new_panel(
                curses.newwin(window_size[0], window_size[1], y_start, 1)
            )
        )
        self.tab().box()
        self.menu = ImportExportMenu(self.tab)
        self.tab().refresh()
        self.user = user
        self.connection = connection
        self.cursor = self.connection.cursor()

    async def proccess_input(self, input_key: int):
        match input_key:
            case Keys.UP:
                self.menu.up_action()
            case Keys.DOWN:
                self.menu.down_action()
            case Keys.ENTER:
                self._handle_enter_input()

    def _handle_enter_input(self) -> None:
        if self.menu.get_choice() == 1:
            imported_passwords = ImportPopup(self.tab, self.user, self.cursor).run()
            if len(imported_passwords) > 0:
                self.connection.commit()
            else:
                self.connection.rollback()
        elif self.menu.get_choice() == 2:
            ExportPopup(self.tab, self.user, self.cursor).run()
        else:
            raise ValueError("Invalid Menu Option")

        self.refresh()

    def show(self):
        self.tab.show()

    def hide(self):
        self.tab.hide()

    def refresh(self):
        self.tab().refresh()
        self.menu.refresh()
