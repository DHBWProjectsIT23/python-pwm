import curses
from src.tui.popup import create_centered_popup
from src.tui.window import Window
from src.tui.panel import Panel

SELECT_CONTROL_STR = """
- ↩ Continue - ↑↓ Select Option -
""".strip()


def show_select_generated_prompt(parent: Panel, title: str) -> tuple[int, Window]:
    padding = create_centered_popup(parent, 12, 60)
    padding().refresh()
    prompt = create_centered_popup(parent, 10, 57)
    prompt().clear()
    select_generate(prompt)
    deselect_own(prompt)
    prompt.writeBottomCenterText(SELECT_CONTROL_STR, (-1, 0))
    prompt().box()
    prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))

    prompt().refresh()

    choice = 1
    while True:
        input_key = prompt().getch()
        match input_key:
            case 65:
                select_generate(prompt)
                deselect_own(prompt)
                prompt().refresh()
                choice = 1
            case 66:
                deselect_generate(prompt)
                select_own(prompt)
                prompt().refresh()
                choice = 2
            case 27:
                prompt().nodelay(True)
                n = prompt().getch()
                prompt().nodelay(False)
                if n == -1:
                    prompt().clear()
                    prompt().refresh()
                    choice = -1
                    break
            case 10:
                break

    return choice, prompt


def select_generate(prompt: Window) -> None:
    prompt.writeCenteredText(" Generate Secure Password ", (-2, 0), curses.A_REVERSE)


def select_own(prompt: Window) -> None:
    prompt.writeCenteredText(" Enter Own Password ", (0, 0), curses.A_REVERSE)


def deselect_generate(prompt: Window) -> None:
    prompt.writeCenteredText(" Generate Secure Password ", (-2, 0))


def deselect_own(prompt: Window) -> None:
    prompt.writeCenteredText(" Enter Own Password ", (0, 0))
