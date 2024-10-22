"""
Module for handling the update password prompt in a terminal user interface.

"""

import curses
from curses.textpad import Textbox
from typing import Optional

from src.crypto.hashing import hash_sha256
from src.crypto.password_util import validate_password_safety
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.user import User
from src.tui.input_validator import InputValidator
from src.tui.panel import Panel
from src.tui.views.overview.components.prompt import Prompt
from src.tui.views.overview.password_tab.add_password_prompt import write_error

CONTROL_STR = " - ↩ Continue - "


def show_update_password_prompt(parent: Panel, user: User) -> Optional[str]:
    """
    Displays a prompt for updating the user's password.

    This function presents a terminal-based interface where the user can
    enter and confirm a new password.
    It performs validations to ensure that the new password is not
    empty, matches the confirmation password,
    is different from the old password, and meets safety standards.

    Args:
        parent (Panel): The parent panel for the prompt,
        which provides the context and display area.
        user (User): The current user object, used to access the existing password for validation.

    Returns:
        Optional[str]: The updated password if successful,
        or None if the operation is cancelled or fails
        due to validation errors.

    Exceptions:
        ExitFromTextBoxException: Raised if the user exits the text box input.

    Process:
        1. Display prompt for the new and confirmed passwords.
        2. Validate that neither field is empty.
        3. Ensure that the passwords match.
        4. Confirm that the new password is different from the current password.
        5. Check that the new password meets safety requirements.
    """
    prompt = Prompt.create_prompt_with_padding(parent)
    title = "Update Password"
    prompt().clear()
    prompt().box()
    prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
    prompt().addstr(3, 2, "    ")
    prompt().addstr(3, 2, "Updated Password:", curses.A_UNDERLINE)
    prompt().addstr(5, 2, "Confirm Password:", curses.A_UNDERLINE)
    prompt.write_bottom_center_text(CONTROL_STR, (-1, 0))

    password_window = prompt().derwin(1, 32, 3, 20)
    confirm_window = prompt().derwin(1, 32, 5, 20)

    password_textbox = Textbox(password_window)
    confirm_textbox = Textbox(confirm_window)

    while True:
        prompt().refresh()
        confirm_window.refresh()
        password_window.refresh()

        curses.curs_set(True)
        try:
            password_textbox.edit(InputValidator.no_spaces_with_exit)
        except ExitFromTextBoxException:
            curses.curs_set(False)
            return None

        password = password_textbox.gather().strip()
        if len(password) == 0:
            write_error("Field can't be empty", prompt, title)

        confirm_window.refresh()

        try:
            confirm_textbox.edit(InputValidator.no_spaces_with_exit)
        except ExitFromTextBoxException:
            return None
        finally:
            curses.curs_set(False)
        confirm = confirm_textbox.gather().strip()
        if len(confirm) == 0:
            write_error("Field can't be empty", prompt, title)
            continue

        if password != confirm:
            write_error("Passwords must match", prompt, title)
            continue

        if hash_sha256(password.encode()) == user.password.password_bytes:
            write_error("Password must be different to before", prompt, title=title)
            continue

        if validate_password_safety(password) < 3:
            write_error("Password is too weak", prompt, title=title)
            continue

        prompt().clear()
        prompt().refresh()
        return password
