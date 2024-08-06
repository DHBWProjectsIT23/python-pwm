import curses
import sqlite3
from src.controller import connection
from src.controller.password import (
    retrieve_password_information,
    update_password_information,
)
from src.controller.user import update_user
from src.crypto.hashing import hash_sha256
from src.model import password_information
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.views.overview.tab_interface import TabInterface
from src.model.user import User
from src.model.password import Password
from src.tui.views.overview.user_tab.update_password_prompt import (
    show_update_password_prompt,
)
from src.tui.views.overview.user_tab.update_username_prompt import UpdateUsernamePrompt


class UserTab(TabInterface):
    def __init__(
        self,
        window_size: tuple[int, int],
        y_start: int,
        user: User,
        connection: sqlite3.Connection,
    ):
        self.tab = Panel(
            curses.panel.new_panel(
                curses.newwin(window_size[0], window_size[1], y_start, 1)
            )
        )
        self.tab().box()

        attr = curses.A_BOLD | curses.A_UNDERLINE
        addstr = self.tab().addstr

        addstr(2, 2, "Username:", attr)

        addstr(4, 2, "Email:", attr)

        self.user = user
        self.connection = connection
        self.cursor = connection.cursor()

        self.tab().refresh()

    async def process_input(self, input_key: int) -> None:
        match input_key:
            case Keys.P | Keys.p:
                self._handle_update_pw_input()
            case Keys.U | Keys.u:
                self._handle_update_uname_input()

    def _handle_update_uname_input(self) -> None:
        new_username = UpdateUsernamePrompt(self.tab, self.cursor, self.user).run()
        if new_username is None:
            return

        password_infos = retrieve_password_information(self.cursor, self.user)
        for pw_info in password_infos:
            if pw_info.data_is_encrypted:
                pw_info.decrypt_data()

        old_username = self.user.username
        self.user.username = hash_sha256(new_username.encode())

        for pw_info in password_infos:
            pw_info.user = self.user
            update_password_information(self.cursor, pw_info, self.user)
            pw_info.decrypt_passwords()

        self.user.username = old_username
        update_user(self.cursor, self.user, new_username.encode())
        self.user.username = new_username.encode()
        self.connection.commit()

    def _handle_update_pw_input(self) -> None:
        new_password_str = show_update_password_prompt(self.tab, self.user)
        if new_password_str is None:
            return

        password_infos = retrieve_password_information(self.cursor, self.user)
        for pw_info in password_infos:
            if pw_info.data_is_encrypted:
                pw_info.decrypt_data()
            pw_info.decrypt_passwords()

        new_password = Password(new_password_str)
        new_password.make_master()
        self.user.password = new_password

        for pw_info in password_infos:
            pw_info.user = self.user
            update_password_information(self.cursor, pw_info, self.user)

        update_user(self.cursor, self.user)
        self.connection.commit()

    def show(self) -> None:
        self.tab.show()

    def hide(self) -> None:
        self.tab.hide()

    def refresh(self) -> None:
        pass
