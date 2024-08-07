import curses

from src.exceptions.encryption_exception import EncryptionException
from src.model.metadata import Metadata
from src.model.password_information import PasswordInformation
from src.tui.panel import Panel
from src.tui.popup import create_centered_popup
from src.tui.window import Window


async def show_details(parent: Panel, password: PasswordInformation) -> None:
    title = "Password Details"
    padding = create_centered_popup(parent, 27, 52)
    padding().refresh()
    popup = create_centered_popup(parent, 25, 50)
    popup().box()
    display_basic_infos(password, popup, title)

    display_categories(password, popup)
    line_amount = display_note(password, popup)

    display_metadata(line_amount, password, popup)

    await display_pwned(password, popup)

    popup().refresh()

    popup().getch()
    popup().clear()
    popup().refresh()


async def display_pwned(password: PasswordInformation, popup: Window) -> None:
    occurences = await password.check_pwned_status()
    y, _ = popup().getyx()
    if occurences == 0:
        popup().addstr(
            y + 2,
            2,
            "Your password has not been pawned!",
            curses.A_ITALIC | curses.color_pair(3),
        )
    else:
        popup().addstr(
            y + 2,
            2,
            f"Your password has been pawned {occurences} times!",
            curses.A_BOLD | curses.color_pair(2),
        )


def display_metadata(
        line_amount: int, password: PasswordInformation, popup: Window
) -> None:
    y = popup().getyx()[0] + line_amount
    metadata = password.metadata
    if not isinstance(metadata, Metadata):
        raise EncryptionException("Metadata of password is still encrypted")
    popup().addstr(y + 2, 1, "Created at:", curses.A_UNDERLINE)
    popup().addstr(f" {metadata.created_at.strftime('%H:%M on %d.%m.%Y')}")
    popup().addstr(y + 4, 1, "Last Modified:", curses.A_UNDERLINE)
    popup().addstr(f" {metadata.last_modified.strftime('%H:%M on %d.%m.%Y')}")


def display_note(password: PasswordInformation, popup: Window) -> int:
    y, _ = popup().getyx()
    popup().addstr(y + 2, 1, "Note:", curses.A_UNDERLINE)
    line_amount = 1
    if password.details.note is not None:
        inset = len("Note: ") + 1
        max_length = (popup().getmaxyx()[1] // 4 * 3) - 2 - inset
        note = password.details.note.decode()
        line_amount = len(note) // max_length + 1
        note_window = popup().derwin(line_amount, max_length, y + 2, inset)
        note_window.addstr(note)
    else:
        popup().addstr(" -")
    return line_amount


def display_categories(password: PasswordInformation, popup: Window) -> None:
    popup().addstr(8, 1, "Categories:", curses.A_UNDERLINE)
    if len(password.details.categories) == 0:
        popup().addstr(" -")
    else:
        y, x = popup().getyx()
        for i, category in enumerate(password.details.categories, 0):
            popup().addstr(y + i, x, f" {category.decode()}")


def display_basic_infos(
        password: PasswordInformation, popup: Window, title: str
) -> None:
    popup().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
    popup().addstr(2, 1, "Description:", curses.A_UNDERLINE)
    popup().addstr(f" {password.description.decode()}")
    popup().addstr(4, 1, "Username:", curses.A_UNDERLINE)
    username = password.details.username or b"-"
    popup().addstr(f" {username.decode()}")
    popup().addstr(6, 1, "Password:", curses.A_UNDERLINE)
    password.decrypt_passwords()
    popup().addstr(f" {password.passwords[-1].password_bytes.decode()}")
