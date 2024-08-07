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
        title: Optional[str] = None,
) -> Optional[str]:
    return show_password_input(
        prompt, password_information, generate_secure_password(), title
    )


def show_password_input(
        prompt: Window,
        password_information: PasswordInformation | None,
        generated_password: str = "",
        title: Optional[str] = None,
) -> Optional[str]:
    prompt().clear()
    prompt().box()
    if title is not None:
        prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
    prompt().addstr(3, 2, "    ")
    prompt().addstr(3, 6, "New Password:", curses.A_UNDERLINE)
    prompt().addstr(5, 2, "Confirm Password:", curses.A_UNDERLINE)
    prompt.write_bottom_center_text(CONTROL_STR, (-1, 0))

    password_textbox, password_window = create_textbox(generated_password,
                                                       3,
                                                       prompt)

    confirm_textbox, confirm_window = create_textbox(generated_password,
                                                     5,
                                                     prompt)

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


def _validate_inputs(confirm: str,
                     password: str,
                     prompt: Window,
                     title: str) -> True:
    if len(confirm) == 0:
        write_error("Field can't be empty", prompt, title)
        return False
    if password != confirm:
        write_error("Passwords must match", prompt, title)
        return False
    return True


def _refresh_all(*args: Window) -> None:
    for window in args:
        window().refresh()


def create_textbox(
        generated_password: str, position: int, prompt: Window
) -> tuple[Textbox, Window]:
    password_window = Window(prompt().derwin(1, 32, position, 20))
    password_window().addstr(0, 0, generated_password)
    password_textbox = Textbox(password_window())
    return password_textbox, password_window


def write_error(msg: str, prompt: Window, title: Optional[str] = None) -> None:
    prompt().box()
    if title is not None:
        prompt().addstr(0, 0, title, curses.color_pair(3) | curses.A_BOLD)
    prompt.write_bottom_center_text(msg, attr=curses.color_pair(2))
    prompt().refresh()
