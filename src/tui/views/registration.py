import curses
import sqlite3
from curses.textpad import Textbox

from src.controller.user import validate_unique_user, insert_user

from ..popup import create_centered_popup
from ..input_validator import InputValidator
from ..util import print_centered_logo
from ..window import Window
from src.model.user import User
from src.crypto.hashing import hash_sha256


def show_registration(
    window: Window, connection: sqlite3.Connection, cursor: sqlite3.Cursor
) -> User:
    print_centered_logo(window, (-9, 0))

    input_window = init_input_window(window)

    username_window = input_window().derwin(1, 32, 2, 20)
    password_window = input_window().derwin(1, 32, 4, 20)
    confirm_window = input_window().derwin(1, 32, 6, 20)

    username_textbox = Textbox(username_window)
    password_textbox = Textbox(password_window)
    confirm_textbox = Textbox(confirm_window)

    password_validator = InputValidator()

    while True:
        input_window().refresh()
        password_window.refresh()
        confirm_window.refresh()
        username_window.refresh()

        curses.curs_set(True)
        username_textbox.edit(InputValidator.no_spaces)
        username: str = username_textbox.gather()
        username = username.strip()

        if len(username) < 4:
            clear_border(input_window)
            show_failed_registration(
                input_window, " Username must have 4 or more characters "
            )
            continue
        if len(username) > 20:
            clear_border(input_window)
            show_failed_registration(
                input_window, " Username must not have more then 20 characters "
            )
            continue
        if not validate_unique_user(cursor, username):
            clear_border(input_window)
            show_failed_registration(input_window, " Username is already taken ")
            continue
        clear_border(input_window)

        password_window.refresh()

        password_validator.reset_password()
        password_textbox.edit(password_validator.password)
        password_str = password_validator.get_password_string().strip()

        confirm_window.refresh()

        password_validator.reset_password()
        confirm_textbox.edit(password_validator.password)
        confirm_str = password_validator.get_password_string().strip()

        window().addstr(5, 5, f"pw: {password_str} - cf: {confirm_str}")
        window().refresh()
        if password_str != confirm_str:
            show_failed_registration(input_window, " Passwords don't match ")
            password_window.clear()
            confirm_window.clear()
            continue
        if len(password_str) < 6:
            clear_border(input_window)
            show_failed_registration(
                input_window, " Password must have 6 or more characters "
            )
            password_window.clear()
            confirm_window.clear()
            continue
        if len(password_str) > 32:
            clear_border(input_window)
            show_failed_registration(
                input_window, " Password must not have more then 32 characters "
            )
            password_window.clear()
            confirm_window.clear()
            continue

        # TODO: Validate Password Strength

        inserted_user = insert_user(cursor, User.new(username, password_str))
        connection.commit()

        if not isinstance(inserted_user, User):
            raise ValueError("Error while inserting User")

        inserted_user.set_clear_password(password_str)
        inserted_user.set_clear_username(username)
        return inserted_user

        # if validate_login(cursor, username, password_str):
        #     show_successful_login(input_window)
        #     return retrieve_user_by_name(cursor, username)
        # else:
        #     show_failed_login(input_window)
        #     password_validator.reset_password()
        #     password_window.clear()
        #     username_window.clear()


def init_input_window(parent: Window) -> Window:
    input_window: Window = create_centered_popup(parent, 9, 57, (1, 0))
    input_window().box()
    input_window().addstr(0, 0, "Registration", curses.A_BOLD)
    input_window().addstr(2, 2, "    New Username:")
    input_window().addstr(4, 2, "    New Password:")
    input_window().addstr(6, 2, "Confirm Password:")
    parent.writeBottomCenterText("- ↲ Continue - ^L Quit - ")
    parent().refresh()
    return input_window


def clear_border(input_window: Window) -> None:
    input_window().box()
    input_window().addstr(0, 0, "Registration", curses.A_BOLD)
    input_window().refresh()


def show_successful_login(input_window: Window) -> None:
    success_message = " Registration successful! "
    input_window().addstr(
        6,
        (35 // 2) - (len(success_message) // 2),
        success_message,
        curses.color_pair(3),
    )
    input_window().refresh()


def show_failed_registration(input_window: Window, message: str) -> None:
    input_window().addstr(
        8,
        (input_window.getSize()[1] // 2) - (len(message) // 2),
        message,
        curses.color_pair(2),
    )
    input_window().refresh()
