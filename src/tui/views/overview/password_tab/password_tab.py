import curses
import sqlite3
from src.tui.keys import Keys
from src.model.password_information import PasswordInformation
from src.tui.util import generate_control_str
from src.tui.views.overview.controls_popup import ControlsPopup
from src.tui.views.overview.password_tab.delete_password_prompt import (
    DeletePasswordPrompt,
)
from src.tui.views.overview.password_tab.history_popup import HistoryPopup
from src.tui.views.overview.password_tab.search_prompt import SearchPrompt
from src.tui.views.overview.tab_interface import TabInterface
from src.tui.window import Window
from src.tui.panel import Panel
from src.tui.views.overview.password_tab.password_list import PasswordList
from src.model.password import Password
from src.tui.views.overview.password_tab.edit_password_prompt import PasswordEditor
from src.tui.views.overview.password_tab.show_details import show_details
from src.model.user import Optional, User
from src.tui.views.overview.password_tab.add_password_prompt import (
    show_add_password_prompt,
)

from src.tui.views.overview.password_tab.create_password_prompt import PasswordCreator
from src.tui.popup import create_centered_popup
from src.controller.password import (
    insert_password_information,
    retrieve_password_information,
    update_password_information,
)


CONTROLS: dict["str", "str"] = {
    "↑↓": "Navigate Passwords",
    "↩": "Show Details",
    "n": "Create new Password",
    "u": "Update Password",
    "e": "Edit Details",
    "d": "Delete Password",
    "r": "Reveal selected Password",
    "R": "Reveal all Passwords",
    "c": "Check if Password has been leaked",
    "C": "Check all Passwords",
    "s": "Search",
    "h": "Display History",
}


class PasswordTab(TabInterface):
    def __init__(
        self,
        window_size: tuple[int, int],
        y_start: int,
        user: User,
        connection: sqlite3.Connection,
    ):
        self.user = user
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.controls = CONTROLS

        self.tab = Panel(
            curses.panel.new_panel(
                curses.newwin(window_size[0], window_size[1], y_start, 1)
            )
        )

        list_width = window_size[1]

        self.list_window = Window(
            self.tab().derwin(window_size[0] - 3, list_width, 0, 0)
        )
        self.tab().box()

        self.password_list = PasswordList(
            self.list_window, retrieve_password_information(self.cursor, self.user)
        )
        self._init_table_headings()

        self.password_list.refresh()
        self.reload_passwords()
        self.refresh()

    def _init_table_headings(self) -> None:
        desc_width, uname_width, pass_width, _ = PasswordList.calculate_columns(
            self.list_window.getSize()[1]
        )
        heading_attr: int = curses.color_pair(4) | curses.A_BOLD | curses.A_UNDERLINE

        self.list_window().addstr(1, 1, "Description/URL", heading_attr)
        self.list_window().addstr(1, desc_width + 1, "Username", heading_attr)
        self.list_window().addstr(
            1, desc_width + uname_width + 1, "Password", heading_attr
        )
        self.list_window().addstr(
            1, desc_width + uname_width + pass_width + 1, "Status", heading_attr
        )
        self.list_window().refresh()

    async def process_input(self, input_key: int) -> None:
        match input_key:
            case Keys.ENTER:
                await show_details(self.tab, self.password_list.get_selected())
                self.refresh()
            case Keys.DOWN:
                self.password_list.select_next()
            case Keys.UP:
                self.password_list.select_previous()
            case Keys.E | Keys.e:
                self._handle_edit_input()
            case Keys.H | Keys.h:
                HistoryPopup(self.tab, self.password_list.get_selected()).run()
                self.refresh()
            case Keys.c:
                await self.password_list.check_selected()
            case Keys.C:
                await self._handle_check_all_input()
            case Keys.D | Keys.d:
                self._handle_delete_password_input()
            case Keys.N | Keys.n:
                self._handle_new_input()

            case Keys.U | Keys.u:
                self._handle_add_input()
            case Keys.r:
                self.password_list.toggle_selected()
            case Keys.R:
                self._handle_reveal_all_input()
            case Keys.S | Keys.s:
                self._handle_search_password_input()
            case Keys.QUESTION_MARK:
                ControlsPopup(self.tab, self.controls).run()
                self.refresh()

    def _handle_add_input(self) -> None:
        password_information = self.password_list.get_selected()
        new_password = show_add_password_prompt(self.tab, password_information)
        if new_password is not None:
            password_information.add_password(Password(new_password))
            update_password_information(self.cursor, password_information, self.user)
            password_information.decrypt_data()
            self.connection.commit()
            self.reload_passwords()

        self.refresh()

    def _handle_new_input(self) -> None:
        new_password = PasswordCreator(self.tab, self.user, self.cursor).run()
        if new_password is not None:
            new_password = insert_password_information(self.cursor, new_password)
            self.connection.commit()
            new_password.decrypt_data()
            self.password_list.add_item(new_password)
            self.reload_passwords()

        self.refresh()

    def _handle_edit_input(self) -> None:
        updated_password = PasswordEditor(self.tab, self.user, self.cursor).run(
            self.password_list.get_selected()
        )
        if updated_password is None:
            self.refresh()
            return

        update_password_information(self.cursor, updated_password, self.user)
        self.connection.commit()
        updated_password.decrypt_data()
        self.password_list.refresh_selected()
        self.reload_passwords()

        self.refresh()

    async def _handle_check_all_input(self) -> None:
        loading_message = "Loading..."
        loading_popup = create_centered_popup(
            self.list_window, 5, len(loading_message) + 4
        )
        loading_popup().box()
        loading_popup.writeCenteredText(loading_message, (0, 0))
        loading_popup().refresh()
        await self.password_list.check_all()

    def _handle_delete_password_input(self) -> None:
        password = self.password_list.get_selected()
        deleted = DeletePasswordPrompt(self.tab, self.user, password, self.cursor).run()
        if deleted:
            self.connection.commit()
            self.reload_passwords()
        else:
            self.refresh()

    def _handle_search_password_input(self) -> None:
        term = SearchPrompt(self.tab, self.user, self.cursor).run()
        if term is None:
            return
        self.reload_passwords(term)
        self.refresh()

    def _handle_reveal_all_input(self) -> None:
        selected = self.password_list.selected
        for item in self.password_list.items:
            item.showing_pass = not item.showing_pass
            item.deselect()
        self.password_list.items[selected].select()
        self.refresh()

    def refresh(self) -> None:
        self.tab().box()
        self._display_controls()
        self.tab().refresh()
        self.list_window().refresh()
        self.password_list.refresh_selected()
        self.password_list.refresh()

    def reload_passwords(self, search_string: Optional[str] = None) -> None:
        passwords = retrieve_password_information(self.cursor, self.user)
        if search_string is not None:
            passwords = list(
                filter(
                    PasswordInformation.create_password_filter(search_string), passwords
                )
            )
        self.password_list = PasswordList(self.list_window, passwords)

    def _display_controls(self) -> None:
        controls_str = generate_control_str(self.controls)
        try:
            self.tab.writeBottomCenterText(controls_str, (-1, 0))
        except ValueError:
            self.tab.writeBottomCenterText("- ? Show Keybinds -", (-1, 0))

    def show(self) -> None:
        self.tab.show()

    def hide(self) -> None:
        self.tab.hide()
