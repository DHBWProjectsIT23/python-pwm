import curses
from typing import Optional
from curses.textpad import Textbox
from src.model.password_information import PasswordInformation
from src.tui.util import no_space_validator
from src.tui.views.overview.select_generated import show_select_generated_prompt
from src.tui.window import Window
from src.tui.panel import Panel
from src.crypto.password_util import generate_secure_password, validate_password_safety


CONTROL_STR = " - ↩ Continue - "


def show_add_password_prompt(
    parent: Panel, password_information: PasswordInformation
) -> Optional[str]:
    choice, prompt = show_select_generated_prompt(parent, "Add Password")
    if choice == 1:
        return show_with_generated(prompt, password_information, "Add Password")
    elif choice == 2:
        return show_password_input(prompt, password_information, title="Add Password")
    elif choice == -1:
        return None
    else:
        raise ValueError("Invalid choice")


def show_with_generated(
    prompt: Window,
    password_information: PasswordInformation,
    title: Optional[str] = None,
) -> str:
    return show_password_input(
        prompt, password_information, generate_secure_password(), title
    )


def show_password_input(
    prompt: Window,
    password_information: PasswordInformation | None,
    generated_password: str = "",
    title: Optional[str] = None,
) -> str:
    prompt().clear()
    prompt().box()
    if title is not None:
        prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
    prompt().addstr(3, 2, "    ")
    prompt().addstr(3, 6, "New Password:", curses.A_UNDERLINE)
    prompt().addstr(5, 2, "Confirm Password:", curses.A_UNDERLINE)
    prompt.writeBottomCenterText(CONTROL_STR, (-1, 0))

    password_window = prompt().derwin(1, 32, 3, 20)
    password_window.addstr(0, 0, generated_password)
    confirm_window = prompt().derwin(1, 32, 5, 20)
    confirm_window.addstr(0, 0, generated_password)

    password_textbox = Textbox(password_window)
    confirm_textbox = Textbox(confirm_window)

    while True:
        prompt().refresh()
        confirm_window.refresh()
        password_window.refresh()

        curses.curs_set(True)
        password_textbox.edit(no_space_validator)
        password = password_textbox.gather().strip()
        if len(password) == 0:
            write_error("Field can't be empty")

        confirm_window.refresh()

        confirm_textbox.edit(no_space_validator)
        confirm = confirm_textbox.gather().strip()
        if len(confirm) == 0:
            write_error("Field can't be empty", prompt, title)

        if password != confirm:
            write_error("Passwords must match", prompt, title)
            continue

        if password_information is not None:
            password_information.decrypt_passwords()
            was_used = False
            for old_password in password_information.passwords:
                if old_password.password.decode() == password:
                    write_error("Password was already used", prompt, title)
                    was_used = True
                    break
            if was_used:
                continue

        # TODO: Validate security
        if validate_password_safety(password) < 3:
            write_error("Password is too weak")
            continue

        prompt().clear()
        prompt().refresh()
        return password


def write_error(msg: str, prompt: Window, title: Optional[str] = None) -> None:
    prompt().box()
    if title is not None:
        prompt().addstr(0, 0, title, curses.color_pair(3) | curses.A_BOLD)
    prompt.writeBottomCenterText(msg, attr=curses.color_pair(2))
    prompt().refresh()
