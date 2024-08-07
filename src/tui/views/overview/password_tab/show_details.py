import curses
from src.model import password_information
from src.model.metadata import Metadata
from src.tui.panel import Panel
from src.model.password_information import PasswordInformation
from src.tui.popup import create_centered_popup
from src.exceptions.encryption_exception import EncryptionException


async def show_details(parent: Panel, password: PasswordInformation) -> None:
    title = "Password Details"
    padding = create_centered_popup(parent, 27, 52)
    padding().refresh()
    popup = create_centered_popup(parent, 25, 50)
    addstr = popup().addstr
    popup().box()
    addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
    addstr(2, 1, "Description:", curses.A_UNDERLINE)
    addstr(f" {password.description.decode()}")
    addstr(4, 1, "Username:", curses.A_UNDERLINE)
    username = password.username or b"-"
    addstr(f" {username.decode()}")
    addstr(6, 1, "Password:", curses.A_UNDERLINE)
    password.decrypt_passwords()
    addstr(f" {password.passwords[-1].password.decode()}")

    addstr(8, 1, "Categories:", curses.A_UNDERLINE)
    if len(password.categories) == 0:
        addstr(" -")
    else:
        y, x = popup().getyx()
        for i, category in enumerate(password.categories, 0):
            addstr(y + i, x, f" {category.decode()}")
    y, _ = popup().getyx()
    addstr(y + 2, 1, "Note:", curses.A_UNDERLINE)
    line_amount = 1
    if password.note is not None:
        inset = len("Note: ") + 1
        max_length = (popup().getmaxyx()[1] // 4 * 3) - 2 - inset
        note = password.note.decode()
        line_amount = len(note) // max_length + 1
        note_window = popup().derwin(line_amount, max_length, y + 2, inset)
        note_window.addstr(note)
    else:
        addstr(" -")

    y = popup().getyx()[0] + line_amount - 1
    metadata = password.metadata
    if not isinstance(metadata, Metadata):
        raise EncryptionException("Metadata of password is still encrypted")

    addstr(y + 2, 1, "Created at:", curses.A_UNDERLINE)
    addstr(f" {metadata.created_at.strftime('%H:%M on %d.%m.%Y')}")

    addstr(y + 4, 1, "Last Modified:", curses.A_UNDERLINE)
    addstr(f" {metadata.last_modified.strftime('%H:%M on %d.%m.%Y')}")

    occurences = await password.check_pwned_status()
    y, _ = popup().getyx()
    if occurences == 0:
        addstr(
            y + 2,
            2,
            "Your password has not been pawned!",
            curses.A_ITALIC | curses.color_pair(3),
        )
    else:
        addstr(
            y + 2,
            2,
            f"Your password has been pawned {occurences} times!",
            curses.A_BOLD | curses.color_pair(2),
        )

    popup().refresh()

    popup().getch()
    popup().clear()
    popup().refresh()
