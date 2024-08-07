import curses
import sqlite3
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.model.user import User
from src.tui.util import generate_control_str
from src.tui.views.overview.controls_popup import ControlsPopup
from src.tui.views.overview.io_tab.export_popup import ExportPopup
from src.tui.views.overview.io_tab.import_export_menu import ImportExportMenu
from src.tui.views.overview.io_tab.import_popup import ImportPopup
from src.tui.views.overview.tab_interface import TabInterface


CONTROLS: dict["str", "str"] = {
    "↑↓": "Navigate Menu",
    "↩": "Select Option",
}


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
        self.controls = CONTROLS

    async def proccess_input(self, input_key: int) -> None:
        match input_key:
            case Keys.UP:
                self.menu.up_action()
            case Keys.DOWN:
                self.menu.down_action()
            case Keys.ENTER:
                self._handle_enter_input()
            case Keys.QUESTION_MARK:
                ControlsPopup(self.tab, self.controls).run()
                self.refresh()

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

    def _display_controls(self) -> None:
        controls_str = generate_control_str(self.controls)
        try:
            self.tab.writeBottomCenterText(controls_str, (-1, 0))
        except ValueError:
            self.tab.writeBottomCenterText("- ? Show Keybinds -", (-1, 0))
        finally:
            self.tab().refresh()

    def show(self) -> None:
        self.tab.show()

    def hide(self) -> None:
        self.tab.hide()

    def refresh(self) -> None:
        self.menu.refresh()
        self._display_controls()
        self.tab().refresh()
