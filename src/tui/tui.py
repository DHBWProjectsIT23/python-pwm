import sqlite3
import curses
import time
from curses.textpad import Textbox, rectangle
from typing import TYPE_CHECKING

from .popup import create_centered_popup
from .util import init_tui, get_screen_size
from src.db.connection import connect_to_db
from src.db.placeholder import validate_login

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


def tui_main(stdscr: Window) -> None:
    init_tui(stdscr)
    connection, cursor = connect_to_db("test.db")
    login_screen(stdscr, cursor)
    time.sleep(5)
    stdscr.clear()
    stdscr.getch()


def first_screen(stdscr: Window) -> None:
    popup = create_centered_popup(stdscr, 7, 35)
    popup.box()
    popup.addstr(0, 0, "Login")
    popup.addstr(2, 2, "New User")


def login_screen(stdscr: Window, cursor: sqlite3.Cursor) -> None:
    logo: str = """
██████  ██████  ██     ██ ███    ███
██   ██ ██   ██ ██     ██ ████  ████
██████  ██████  ██  █  ██ ██ ████ ██
██      ██      ██ ███ ██ ██  ██  ██
██      ██       ███ ███  ██      ██
 """.strip()
    logo_caption = " Python Password Manager "
    logo_lines = logo.split("\n")
    logo_height = len(logo_lines)
    logo_width = max(len(line) for line in logo_lines)
    caption_width = len(logo_caption)
    max_screen_height, max_screen_width = get_screen_size(stdscr)

    logo_start_y = (max_screen_height // 2) - (logo_height // 2) - 9
    logo_start_x = (max_screen_width // 2) - (logo_width // 2)

    caption_start_y = logo_start_y + logo_height + 1
    caption_start_x = (max_screen_width // 2) - (caption_width // 2)

    for i, line in enumerate(logo_lines):
        stdscr.addstr(logo_start_y + i, logo_start_x, line, curses.color_pair(5))

    stdscr.addstr(
        caption_start_y,
        caption_start_x,
        logo_caption,
        curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE,
    )

    stdscr.refresh()
    popup = create_centered_popup(stdscr, 7, 35)
    popup.box()
    popup.addstr(0, 0, "Login")
    popup.addstr(2, 2, "Username:")
    popup.addstr(4, 2, "Password:")

    popup.refresh()

    username_window = popup.derwin(1, 15, 2, 12)
    password_window = popup.derwin(1, 15, 4, 12)

    popup.refresh()

    username_textbox = Textbox(username_window)

    popup.refresh()

    password: list[str] = []

    def validate_password(ch: int) -> int:
        if ch == 10:
            return 7

        if ch in (curses.KEY_BACKSPACE, curses.KEY_DC):
            password.pop()
            return curses.KEY_BACKSPACE

        if 32 <= ch <= 126:
            password.append(chr(ch))
            return 42

        return ch

    password_textbox = Textbox(password_window)

    logged_in = False
    while not logged_in:
        curses.curs_set(True)
        username_textbox.edit()
        username: str = username_textbox.gather()
        password_textbox.edit(validate_password)
        password_str: str = "".join(password).strip()
        username = username.strip()
        popup.box()
        popup.addstr(0, 0, "Login")
        curses.curs_set(False)

        validating_message = " Login successful! "
        wrong_password_or_username = " Wrong username or password "
        if validate_login(cursor, username, password_str):
            popup.addstr(
                6,
                (35 // 2) - (len(validating_message) // 2),
                validating_message,
                curses.color_pair(3),
            )
            logged_in = True
            popup.refresh()
        else:
            popup.addstr(
                6,
                (35 // 2) - (len(wrong_password_or_username) // 2),
                wrong_password_or_username,
                curses.color_pair(2),
            )
            password_window.clear()
            username_window.clear()
            password = []
            popup.refresh()
