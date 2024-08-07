import curses
import sqlite3
from curses.textpad import Textbox

from src.controller.user import retrieve_user_by_name
from src.controller.user import validate_login
from src.model.user import User
from ..input_validator import InputValidator
from ..popup import create_centered_popup
from ..util import print_centered_logo
from ..window import Window


def show_login(window: Window, cursor: sqlite3.Cursor) -> User:
    print_centered_logo(window, (-9, 0))

    input_window = init_input_window(window)

    username_window = input_window().derwin(1, 32, 2, 12)
    password_window = input_window().derwin(1, 32, 4, 12)

    username_textbox = Textbox(username_window)
    password_textbox = Textbox(password_window)

    validator = InputValidator()

    while True:
        input_window().refresh()
        password_window.refresh()

        curses.curs_set(True)
        username_textbox.edit(InputValidator.no_spaces)
        username: str = username_textbox.gather()
        username = username.strip()

        username_window.refresh()
        password_window.refresh()

        password_textbox.edit(validator.password)
        password_str = validator.get_password_string().strip()

        input_window().box()

        if validate_login(cursor, username, password_str):
            show_successful_login(input_window)
            user = retrieve_user_by_name(cursor, username)
            user.set_clear_password(password_str)
            user.set_clear_username(username)
            return user

        show_failed_login(input_window)
        validator.reset_password()
        password_window.clear()
        username_window.clear()


def init_input_window(parent: Window) -> Window:
    input_window: Window = create_centered_popup(parent, 7, 57)
    input_window().box()
    input_window().addstr(0, 0, "Login", curses.A_BOLD)
    input_window().addstr(2, 2, "Username:")
    input_window().addstr(4, 2, "Password:")
    parent.write_bottom_center_text("- ↲ Continue - ^L Quit - ")
    parent().refresh()
    return input_window


def show_successful_login(input_window: Window) -> None:
    login_success_message = " Login successful! "
    input_window().addstr(
        6,
        (35 // 2) - (len(login_success_message) // 2),
        login_success_message,
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
