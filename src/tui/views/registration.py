"""
This module handles user registration for a terminal-based application, 
including user input validation and database insertion.
"""
import curses
import sqlite3
from curses.textpad import Textbox

from src.controller.user import insert_user
from src.controller.user import validate_unique_user
from src.crypto.password_util import validate_password_safety
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.popup import create_centered_popup
from src.tui.util import print_centered_logo
from src.tui.window import Window


def show_registration(
    window: Window, connection: sqlite3.Connection, cursor: sqlite3.Cursor
) -> User:
    """
    Displays the registration screen, handles user input for username, password,
    and password confirmation. Validates the input and creates a new user if
    the registration is successful.

    Args:
        window (Window): The Window object used for displaying the registration screen.
        connection (sqlite3.Connection): The database connection used for inserting the new user.
        cursor (sqlite3.Cursor): The database cursor for executing queries.

    Returns:
        User: The User object representing the newly registered user.

    Raises:
        ValueError: If there is an error while inserting the user into the database.
    """
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
    """
    Finalizes the user registration by inserting the new user into the database
    and returning the User object.

    Args:
        connection (sqlite3.Connection): The database connection used for inserting the new user.
        password_str (str): The user's password.
        username (str): The user's username.

    Returns:
        User: The User object representing the newly registered user.

    Raises:
        ValueError: If there is an error while inserting the user into the database.
    """
    inserted_user = insert_user(connection.cursor(), User.new(username, password_str))
    connection.commit()
    if not isinstance(inserted_user, User):
        raise ValueError("Error while inserting User")
    inserted_user.set_clear_password(password_str)
    inserted_user.set_clear_username(username)
    return inserted_user


def _refresh_all(*args: Window) -> None:
    """
    Refreshes all provided Window objects.

    Args:
        *args (Window): The Window objects to be refreshed.
    """
    for window in args:
        window().refresh()


def _create_textbox(input_window: Window, position: int) -> tuple[Textbox, Window]:
    """
    Creates a Textbox and its associated Window object at the specified position.

    Args:
        input_window (Window): The parent Window object used to create the new Textbox window.
        position (int): The y-coordinate position of the new Textbox within the parent window.

    Returns:
        tuple[Textbox, Window]: A tuple containing the created Textbox and its Window object.
    """
    username_window = Window(input_window().derwin(1, 32, position, 20))
    username_textbox = Textbox(username_window())
    return username_textbox, username_window


def init_input_window(parent: Window) -> Window:
    """
    Initializes and creates the input window for the registration screen, centered
    on the parent window.

    Args:
        parent (Window): The parent Window object used to center the input window.

    Returns:
        Window: A Window object representing the centered input window.
    """
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
    """
    Clears and redraws the border of the input window, including the title.

    Args:
        input_window (Window): The Window object whose border is to be cleared and redrawn.
    """
    input_window().box()
    input_window().addstr(0, 0, "Registration", curses.A_BOLD)
    input_window().refresh()


def show_successful_register(input_window: Window) -> None:
    """
    Displays a message indicating that the registration was successful.

    Args:
        input_window (Window): The Window object where the success message will be shown.
    """
    register_success_message = " Registration successful! "
    input_window.write_bottom_center_text(
        register_success_message,
    )
    input_window().refresh()


def show_failed_registration(
    input_window: Window, register_failed_message: str
) -> None:
    """
    Displays a message indicating that the registration failed due to the given reason.

    Args:
        input_window (Window): The Window object where the failure message will be shown.
        register_failed_message (str): The message to display indicating why registration failed.
    """
    input_window.write_bottom_center_text(
        register_failed_message,
        attr=curses.color_pair(2),
    )
    input_window().refresh()
