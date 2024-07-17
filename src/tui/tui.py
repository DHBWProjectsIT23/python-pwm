import sqlite3
import curses
import time
from curses.textpad import Textbox
from typing import TYPE_CHECKING

from .popup import create_centered_popup
from .util import init_tui
from .window import Window
from src.db.connection import connect_to_db
from src.db.placeholder import validate_login

if TYPE_CHECKING:
    from _curses import _CursesWindow

    CursesWindow = _CursesWindow
else:
    from typing import Any

    CursesWindow = Any


def tui_main(stdscr: CursesWindow) -> None:
    window: Window = init_tui(stdscr)
    connection, cursor = connect_to_db("test.db")
    login_screen(window, cursor)
    time.sleep(5)
    window().clear()
    window().getch()


def login_screen(window: Window, cursor: sqlite3.Cursor) -> None:
    logo: str = """
██████  ██████  ██     ██ ███    ███
██   ██ ██   ██ ██     ██ ████  ████
██████  ██████  ██  █  ██ ██ ████ ██
██      ██      ██ ███ ██ ██  ██  ██
██      ██       ███ ███  ██      ██
 """.strip()
    logo_caption = " Python Password Manager "

    window.writeCenteredMultilineText(logo, (-9, 0), curses.color_pair(5))
    window.writeCenteredText(
        logo_caption, (-5, 0), curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE
    )
    window().refresh()

    popup: Window = create_centered_popup(window, 7, 35)
    popup().box()
    popup().addstr(0, 0, "Login")
    popup().addstr(2, 2, "Username:")
    popup().addstr(4, 2, "Password:")

    username_window = popup().derwin(1, 15, 2, 12)
    password_window = popup().derwin(1, 15, 4, 12)

    username_textbox = Textbox(username_window)

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
        popup().refresh()
        curses.curs_set(True)
        username_textbox.edit()
        username: str = username_textbox.gather()
        password_textbox.edit(validate_password)
        password_str: str = "".join(password).strip()
        username = username.strip()
        popup().box()
        popup().addstr(0, 0, "Login")
        curses.curs_set(False)

        validating_message = " Login successful! "
        wrong_password_or_username = " Wrong username or password "
        if validate_login(cursor, username, password_str):
            popup().addstr(
                6,
                (35 // 2) - (len(validating_message) // 2),
                validating_message,
                curses.color_pair(3),
            )
            logged_in = True
            popup().refresh()
        else:
            popup().addstr(
                6,
                (35 // 2) - (len(wrong_password_or_username) // 2),
                wrong_password_or_username,
                curses.color_pair(2),
            )
            password_window.clear()
            username_window.clear()
            password = []
            popup().refresh()
