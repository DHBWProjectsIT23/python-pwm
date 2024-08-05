import curses
from src.model import password_information
from src.tui.panel import Panel
from src.model.password_information import PasswordInformation
from src.tui.popup import create_centered_popup


async def show_details(parent: Panel, password: PasswordInformation) -> None:
    title = "Password Details"
    padding = create_centered_popup(parent, 22, 52)
    padding().refresh()
    popup = create_centered_popup(parent, 22, 50)
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
    if password.note is not None:
        note = password.note.decode()
        inset = len("Note: ") + 1
        max_length = (popup().getmaxyx()[1] // 4 * 3) - 2 - inset
        line_amount = len(note) // max_length
        lines: list[str] = []
        position = 0
        for i in range(line_amount):
            if position + max_length >= len(note):
                break
            lines.append(note[position : position + max_length])
            position += max_length

        for i, line in enumerate(lines):
            addstr(y + 2 + i, inset, line)

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
