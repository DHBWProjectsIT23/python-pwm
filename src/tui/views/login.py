"""
Handles the login screen of the terminal user interface, including user input for credentials,
validation of login information, and display of success or error messages.
"""

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
    """
    Displays the login screen, handles user input for username and password,
    and validates the login credentials.

    Args:
        window (Window): The Window object used for displaying the login screen.
        cursor (sqlite3.Cursor): The database cursor for executing queries.

    Returns:
        User: The User object associated with the successfully logged-in user.

    Raises:
        ValueError: If the login attempt fails or the username/password validation fails.
    """
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
    """
    Initializes and creates the input window for the login screen, centered
    on the parent window.

    Args:
        parent (Window): The parent Window object used to center the input window.

    Returns:
        Window: A Window object representing the centered input window.
    """
    input_window: Window = create_centered_popup(parent, 7, 57)
    input_window().box()
    input_window().addstr(0, 0, "Login", curses.A_BOLD)
    input_window().addstr(2, 2, "Username:")
    input_window().addstr(4, 2, "Password:")
    parent.write_bottom_center_text("- ↲ Continue - ^L Quit - ")
    parent().refresh()
    return input_window


def show_successful_login(input_window: Window) -> None:
    """
    Displays a message indicating that the login was successful.

    Args:
        input_window (Window): The Window object where the success message will be shown.
    """
    login_success_message = " Login successful! "
    input_window.write_bottom_center_text(
        login_success_message,
        attr=curses.color_pair(3),
    )
    input_window().refresh()


def show_failed_login(input_window: Window) -> None:
    """
    Displays a message indicating that the login attempt failed due to
    incorrect username or password.

    Args:
        input_window (Window): The Window object where the failure message will be shown.
    """
    wrong_password_or_username = " Wrong username or password "
    input_window.write_bottom_center_text(
        wrong_password_or_username,
        attr=curses.color_pair(2),
    )
    input_window().refresh()
