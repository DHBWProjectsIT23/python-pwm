"""
Module for displaying prompts for adding passwords in a terminal user interface.
Includes functions for showing password input fields and validating passwords.
"""
import curses
from curses.textpad import Textbox
from typing import Optional

from src.crypto.password_util import generate_secure_password
from src.crypto.password_util import validate_password_safety
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.password_information import PasswordInformation
from src.tui.input_validator import InputValidator
from src.tui.panel import Panel
from src.tui.views.overview.password_tab.show_generate_menu import (
    show_select_generated_prompt,
)
from src.tui.window import Window

TITLE = "Add Password"

CONTROL_STR = " - ↩ Continue - "


def show_add_password_prompt(
    parent: Panel, password_information: PasswordInformation
) -> Optional[str]:
    """
    Displays a prompt to the user to add a new password. 
    Offers options to generate a secure password
    or enter a password manually. Handles user choice and returns the password.

    Args:
        parent (Panel): The parent panel for the prompt.
        password_information (PasswordInformation): An object to store the new password information.

    Returns:
        Optional[str]: The entered or generated password, or None if the operation is cancelled.
    """
    choice, prompt = show_select_generated_prompt(parent, TITLE)
    if choice == 1:
        return show_with_generated(prompt, password_information, TITLE)
    if choice == 2:
        return show_password_input(prompt, password_information, title=TITLE)
    if choice == -1:
        return None
    raise ValueError("Invalid choice")


def show_with_generated(
    prompt: Window,
    password_information: PasswordInformation,
    title: str = "",
) -> Optional[str]:
    """
    Displays a prompt where a secure password is generated and shown to the user. The user is then
    prompted to confirm or enter the password. 

    Args:
        prompt (Window): The window used to display the prompt.
        password_information (PasswordInformation): An object to store the new password information.
        title (str, optional): The title of the prompt. Defaults to an empty string.

    Returns:
        Optional[str]: The generated password, or None if the operation is cancelled.
    """
    return show_password_input(
        prompt, password_information, generate_secure_password(), title
    )


def show_password_input(
    prompt: Window,
    password_information: PasswordInformation | None,
    generated_password: str = "",
    title: str = "",
) -> Optional[str]:
    """
    Displays a prompt for the user to enter a new password and 
    confirm it. Validates the entered passwords
    and checks their strength and uniqueness.

    Args:
        prompt (Window): The window used to display the prompt.
        password_information (Optional[PasswordInformation]): 
        An object to store the new password information.
        generated_password (str, optional): 
        A pre-generated password to show as default. Defaults to an empty string.
        title (str, optional): The title of the prompt. Defaults to an empty string.

    Returns:
        Optional[str]: The entered password, or None if the operation is cancelled.
    """
    prompt().clear()
    prompt().box()
    prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
    prompt().addstr(3, 2, "    ")
    prompt().addstr(3, 6, "New Password:", curses.A_UNDERLINE)
    prompt().addstr(5, 2, "Confirm Password:", curses.A_UNDERLINE)
    prompt.write_bottom_center_text(CONTROL_STR, (-1, 0))

    password_textbox, password_window = create_textbox(generated_password, 3, prompt)

    confirm_textbox, confirm_window = create_textbox(generated_password, 5, prompt)

    while True:
        _refresh_all(prompt, confirm_window, password_window)

        curses.curs_set(True)
        try:
            password_textbox.edit(InputValidator.no_spaces_with_exit)
            password = password_textbox.gather().strip()
            if len(password) == 0:
                write_error("Field can't be empty", prompt, title)

            confirm_window().refresh()

            confirm_textbox.edit(InputValidator.no_spaces_with_exit)
            confirm = confirm_textbox.gather().strip()
            if not _validate_inputs(confirm, password, prompt, title):
                continue

            if password_information is not None:
                password_information.decrypt_passwords()
                was_used = False
                for old_password in password_information.passwords:
                    if old_password.password_bytes.decode() == password:
                        write_error("Password was already used", prompt, title)
                        was_used = True
                        break
                if was_used:
                    continue

            if validate_password_safety(password) < 3:
                write_error("Password is too weak", prompt, title)
                continue
        except ExitFromTextBoxException:
            return None
        finally:
            curses.curs_set(False)

        prompt().clear()
        prompt().refresh()
        return password


def _validate_inputs(confirm: str, password: str, prompt: Window, title: str) -> bool:
    """
    Validates the password and confirmation password. 
    Checks that neither is empty and that they match.

    Args:
        confirm (str): The confirmation password entered by the user.
        password (str): The new password entered by the user.
        prompt (Window): The window used to display the prompt.
        title (str): The title of the prompt.

    Returns:
        bool: True if the inputs are valid, otherwise False.
    """
    if len(confirm) == 0:
        write_error("Field can't be empty", prompt, title)
        return False
    if password != confirm:
        write_error("Passwords must match", prompt, title)
        return False
    return True


def _refresh_all(*args: Window) -> None:
    """
    Refreshes all provided windows.

    Args:
        *args (Window): The windows to refresh.
    """

    for window in args:
        window().refresh()


def create_textbox(
    generated_password: str, position: int, prompt: Window
) -> tuple[Textbox, Window]:
    """
    Creates a textbox for password entry with optional pre-filled text.

    Args:
        generated_password (str): An optional pre-generated password to fill the textbox.
        position (int): The vertical position of the textbox in the prompt window.
        prompt (Window): The window used to display the prompt.

    Returns:
        tuple[Textbox, Window]: The created Textbox and its associated Window.
    """
    password_window = Window(prompt().derwin(1, 32, position, 20))
    password_window().addstr(0, 0, generated_password)
    password_textbox = Textbox(password_window())
    return password_textbox, password_window


def write_error(msg: str, prompt: Window, title: Optional[str] = None) -> None:
    """
    Displays an error message in the prompt window.

    Args:
        msg (str): The error message to display.
        prompt (Window): The window used to display the prompt.
        title (Optional[str], optional): The title of the prompt. Defaults to None.
    """
    prompt().box()
    if title is not None:
        prompt().addstr(0, 0, title, curses.color_pair(3) | curses.A_BOLD)
    prompt.write_bottom_center_text(msg, attr=curses.color_pair(2))
    prompt().refresh()
