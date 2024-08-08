import curses
import sqlite3
from curses.textpad import Textbox

from src.controller.user import insert_user
from src.controller.user import validate_unique_user
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.popup import create_centered_popup
from src.crypto.password_util import validate_password_safety
from src.tui.util import print_centered_logo
from src.tui.window import Window


def show_registration(
    window: Window, connection: sqlite3.Connection, cursor: sqlite3.Cursor
) -> User:
    print_centered_logo(window, (-9, 0))

    input_window = init_input_window(window)

    username_textbox, username_window = _create_textbox(input_window, 2)

    password_textbox, password_window = _create_textbox(input_window, 4)

    confirm_textbox, confirm_window = _create_textbox(input_window, 6)

    password_validator = InputValidator()

    while True:
        _refresh_all(confirm_window, input_window, password_window, username_window)

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

        password_window().refresh()

        password_validator.reset_password()
        password_textbox.edit(password_validator.password)
        password_str = password_validator.get_password_string().strip()

        confirm_window().refresh()

        password_validator.reset_password()
        confirm_textbox.edit(password_validator.password)
        confirm_str = password_validator.get_password_string().strip()

        window().addstr(5, 5, f"pw: {password_str} - cf: {confirm_str}")
        window().refresh()
        if password_str != confirm_str:
            show_failed_registration(input_window, " Passwords don't match ")
            password_window().clear()
            confirm_window().clear()
            continue

        if validate_password_safety(password_str) < 3:
            show_failed_registration(input_window, "Password is too weak")
            continue

        return _finalize_user(connection, password_str, username)


def _finalize_user(
    connection: sqlite3.Connection, password_str: str, username: str
) -> User:
    inserted_user = insert_user(connection.cursor(), User.new(username, password_str))
    connection.commit()
    if not isinstance(inserted_user, User):
        raise ValueError("Error while inserting User")
    inserted_user.set_clear_password(password_str)
    inserted_user.set_clear_username(username)
    return inserted_user


def _refresh_all(*args: Window) -> None:
    for window in args:
        window().refresh()


def _create_textbox(input_window: Window, position: int) -> tuple[Textbox, Window]:
    username_window = Window(input_window().derwin(1, 32, position, 20))
    username_textbox = Textbox(username_window())
    return username_textbox, username_window


def init_input_window(parent: Window) -> Window:
    input_window: Window = create_centered_popup(parent, 9, 57, (1, 0))
    input_window().box()
    input_window().addstr(0, 0, "Registration", curses.A_BOLD)
    input_window().addstr(2, 2, "    New Username:")
    input_window().addstr(4, 2, "    New Password:")
    input_window().addstr(6, 2, "Confirm Password:")
    parent.write_bottom_center_text("- ↲ Continue - ^L Quit - ")
    parent().refresh()
    return input_window


def clear_border(input_window: Window) -> None:
    input_window().box()
    input_window().addstr(0, 0, "Registration", curses.A_BOLD)
    input_window().refresh()


def show_successful_register(input_window: Window) -> None:
    register_success_message = " Registration successful! "
    input_window.write_bottom_center_text(
        register_success_message,
    )
    input_window().refresh()


def show_failed_registration(
    input_window: Window, register_failed_message: str
) -> None:
    input_window.write_bottom_center_text(
        register_failed_message,
        attr=curses.color_pair(2),
    )
    input_window().refresh()
