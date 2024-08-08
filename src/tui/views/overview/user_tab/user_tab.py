import curses
import sqlite3
import sys

from src.controller.password import retrieve_password_information
from src.controller.password import update_password_information
from src.controller.user import update_user
from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.user import User
from src.tui.keys import Keys
from src.tui.popup import create_centered_popup
from src.tui.util import percentage_of
from src.tui.views.overview.components.controls_popup import ControlsPrompt
from src.tui.views.overview.components.tab_interface import TabInterface
from src.tui.views.overview.user_tab.delete_user_prompt import DeleteUserPrompt
from src.tui.views.overview.user_tab.update_password_prompt import (
    show_update_password_prompt,
)
from src.tui.views.overview.user_tab.update_username_prompt import UpdateUsernamePrompt

CONTROLS: dict["str", "str"] = {
    "u": "Change Username",
    "p": "Change Password",
    "d": "Delete User",
}


class UserTab(TabInterface):
    def __init__(
        self,
        window_size: tuple[int, int],
        y_start: int,
        user: User,
        connection: sqlite3.Connection,
    ):
        super().__init__(window_size, y_start, CONTROLS)
        self.tab().box()

        self.user = user
        self.connection = connection
        self.cursor = connection.cursor()
        self.controls = CONTROLS

        self.refresh()

    async def process_input(self, input_key: int) -> None:
        match input_key:
            case Keys.D | Keys.D_LOWER:
                self._handle_delete_user_input()
            case Keys.P | Keys.P_LOWER:
                self._handle_update_pw_input()
            case Keys.U | Keys.U_LOWER:
                self._handle_update_uname_input()
            case Keys.QUESTION_MARK:
                ControlsPrompt(self.tab, self.controls).run()
                self.refresh()

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
            update_password_information(self.cursor, pw_info)
            pw_info.decrypt_passwords()

        update_user(self.cursor, self.user, old_username)
        self.user.set_clear_username(new_username)
        self.connection.commit()
        self.refresh()

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
            update_password_information(self.cursor, pw_info)

        update_user(self.cursor, self.user)
        self.user.set_clear_password(new_password_str)
        self.connection.commit()

    def _handle_delete_user_input(self) -> None:
        deleted = DeleteUserPrompt(self.tab, self.user, self.cursor).run()
        if deleted:
            self.connection.commit()
            sys.exit(0)
        self.refresh()

    def _display_user_info(self) -> None:
        height = percentage_of(70, self.tab.get_size()[0])
        width = percentage_of(70, self.tab.get_size()[1])

        info_display = create_centered_popup(self.tab, height, width)

        data_inset = 20

        attr = curses.A_BOLD | curses.A_UNDERLINE
        addstr = info_display().addstr

        addstr(2, 2, "Username:", attr)
        try:
            addstr(2, data_inset, f"{self.user.get_clear_username()}")
        except ValueError:
            addstr(
                2,
                data_inset,
                "Failed to load username",
                curses.A_ITALIC | curses.color_pair(2),
            )

        addstr(4, 2, "No. of Passwords:", attr)
        addstr(
            4,
            data_inset,
            f"{len(retrieve_password_information(self.cursor, self.user))}",
        )
        info_display().refresh()

    def refresh(self) -> None:
        self._display_user_info()
        self._display_controls()
        self.tab().refresh()
