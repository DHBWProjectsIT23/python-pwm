import curses
import sqlite3
from curses.textpad import Textbox

from src.controller.user import retrieve_user_by_name, validate_login
from src.model.user import User

from ..password_input_validator import PasswordInputValidator
from ..popup import create_centered_popup
from ..util import no_space_validator, print_centered_logo
from ..window import Window


def show_login(window: Window, cursor: sqlite3.Cursor) -> User:
    print_centered_logo(window, (-9, 0))

    input_window = init_input_window(window)

    username_window = input_window().derwin(1, 32, 2, 12)
    password_window = input_window().derwin(1, 32, 4, 12)

    username_textbox = Textbox(username_window)
    password_textbox = Textbox(password_window)

    password_validator = PasswordInputValidator()

    while True:
        input_window().refresh()
        password_window.refresh()

        curses.curs_set(True)
        username_textbox.edit(no_space_validator)
        username: str = username_textbox.gather()
        username = username.strip()

        username_window.refresh()
        password_window.refresh()

        password_textbox.edit(password_validator)
        password_str = password_validator.get_password_string().strip()

        input_window().box()

        if validate_login(cursor, username, password_str):
            show_successful_login(input_window)
            user = retrieve_user_by_name(cursor, username)
            user.set_clear_password(password_str)
            return user

        show_failed_login(input_window)
        password_validator.reset_password()
        password_window.clear()
        username_window.clear()


def init_input_window(parent: Window) -> Window:
    input_window: Window = create_centered_popup(parent, 7, 57)
    input_window().box()
    input_window().addstr(0, 0, "Login", curses.A_BOLD)
    input_window().addstr(2, 2, "Username:")
    input_window().addstr(4, 2, "Password:")
    parent.writeBottomCenterText("- ↲ Continue - ^L Quit - ")
    parent().refresh()
    return input_window


def show_successful_login(input_window: Window) -> None:
    success_message = " Login successful! "
    input_window().addstr(
        6,
        (35 // 2) - (len(success_message) // 2),
        success_message,
        curses.color_pair(3),
    )
    input_window().refresh()


def show_failed_login(input_window: Window) -> None:
    wrong_password_or_username = " Wrong username or password "
    input_window().addstr(
        6,
        (35 // 2) - (len(wrong_password_or_username) // 2),
        wrong_password_or_username,
        curses.color_pair(2),
    )
    input_window().refresh()
