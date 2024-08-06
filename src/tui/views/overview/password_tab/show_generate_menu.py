import curses
from src.tui.views.overview.prompt import Prompt
from src.tui.window import Window
from src.tui.panel import Panel

SELECT_CONTROL_STR = """
- ↩ Continue - ↑↓ Select Option -
""".strip()


def show_select_generated_prompt(parent: Panel, title: str) -> tuple[int, Window]:
    prompt = Prompt.create_prompt_with_padding(parent)
    _select_generate(prompt)
    _deselect_own(prompt)
    prompt.writeBottomCenterText(SELECT_CONTROL_STR, (-1, 0))
    prompt().box()
    prompt().addstr(0, 0, title, curses.A_BOLD | curses.color_pair(3))

    prompt().refresh()

    choice = 1
    while True:
        input_key = prompt().getch()
        match input_key:
            case 65:
                _select_generate(prompt)
                _deselect_own(prompt)
                prompt().refresh()
                choice = 1
            case 66:
                _deselect_generate(prompt)
                _select_own(prompt)
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


def _select_generate(prompt: Window) -> None:
    prompt.writeCenteredText(" Generate Secure Password ", (-2, 0), curses.A_REVERSE)


def _select_own(prompt: Window) -> None:
    prompt.writeCenteredText(" Enter Own Password ", (0, 0), curses.A_REVERSE)


def _deselect_generate(prompt: Window) -> None:
    prompt.writeCenteredText(" Generate Secure Password ", (-2, 0))


def _deselect_own(prompt: Window) -> None:
    prompt.writeCenteredText(" Enter Own Password ", (0, 0))
