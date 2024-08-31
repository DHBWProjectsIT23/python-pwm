"""
Module for displaying detailed information about a password.
"""
import curses

from src.exceptions.encryption_exception import EncryptionException
from src.model.metadata import Metadata
from src.model.password_information import PasswordInformation
from src.tui.panel import Panel
from src.tui.popup import create_centered_popup
from src.tui.window import Window


async def show_details(parent: Panel, password: PasswordInformation) -> None:
    """
    Displays detailed information about the given password in a popup window.

    This function creates and displays a centered popup showing various details about the
    provided password, including basic information, categories, notes, metadata, and pwned
    status. It waits for the user to press a key before closing the popup.

    Args:
        parent (Panel): The parent panel where the popup will be displayed.
        password (PasswordInformation): The password object containing the details to be shown.
    """
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
    """
    Displays the pwned status of the given password in the popup window.

    This function asynchronously checks the pwned status of the password and displays
    the result in the popup window. It indicates whether the password has been pwned and
    how many times, using different colors and styles for the text.

    Args:
        password (PasswordInformation): The password object whose pwned status will be checked.
        popup (Window): The popup window where the pwned status will be displayed.
    """
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
    """
    Displays metadata related to the password in the popup window.

    This function adds information about the creation and last modification times of the password
    to the popup window. It ensures that metadata is decrypted before displaying it.

    Args:
        line_amount (int): The number of lines used by the note section 
        to correctly position the metadata.
        password (PasswordInformation): The password object containing the metadata to be displayed.
        popup (Window): The popup window where the metadata will be displayed.
    
    Raises:
        EncryptionException: If the password metadata is still encrypted.
    """
    y = popup().getyx()[0] + line_amount
    metadata = password.metadata
    if not isinstance(metadata, Metadata):
        raise EncryptionException("Metadata of password is still encrypted")
    popup().addstr(y + 2, 1, "Created at:", curses.A_UNDERLINE)
    popup().addstr(f" {metadata.created_at.strftime('%H:%M on %d.%m.%Y')}")
    popup().addstr(y + 4, 1, "Last Modified:", curses.A_UNDERLINE)
    popup().addstr(f" {metadata.last_modified.strftime('%H:%M on %d.%m.%Y')}")


def display_note(password: PasswordInformation, popup: Window) -> int:
    """
    Displays any notes associated with the password in the popup window.

    This function extracts and formats the note associated with the password, and displays
    it in the popup window. It handles cases where the note may span multiple lines.

    Args:
        password (PasswordInformation): The password object containing the note to be displayed.
        popup (Window): The popup window where the note will be displayed.

    Returns:
        int: The number of lines used by the note section.
    """
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
    """
    Displays categories associated with the password in the popup window.

    This function adds the categories associated with the password to the popup window. It
    displays each category on a new line.

    Args:
        password (PasswordInformation): The password object containing categories to be displayed.
        popup (Window): The popup window where the categories will be displayed.
    """
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
    """
    Displays basic information about the password in the popup window.

    This function shows the description, username, and password in the popup window. It also
    formats and styles the information for better readability.

    Args:
        password (PasswordInformation): The password object containing 
        the basic details to be displayed.
        popup (Window): The popup window where the basic information 
        will be displayed.
        title (str): The title to be displayed at the top of the popup window.
    """
    popup().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))
    popup().addstr(2, 1, "Description:", curses.A_UNDERLINE)
    popup().addstr(f" {password.details.description.decode()}")
    popup().addstr(4, 1, "Username:", curses.A_UNDERLINE)
    username = password.details.username or b"-"
    popup().addstr(f" {username.decode()}")
    popup().addstr(6, 1, "Password:", curses.A_UNDERLINE)
    password.decrypt_passwords()
    popup().addstr(f" {password.passwords[-1].password_bytes.decode()}")
