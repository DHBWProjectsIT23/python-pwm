from __future__ import annotations

import asyncio
import curses
from typing import TYPE_CHECKING

from src.model.password_information import PasswordInformation
from src.tui.util import pad_with
from src.tui.util import percentage_of
from src.tui.util import shorten_str
from src.tui.window import Window

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Pad = _CursesWindow
    CursesWindow = _CursesWindow
else:
    from typing import Any

    Pad = Any
    CursesWindow = Any


class PasswordList:
    def __init__(self,
                 parent: Window,
                 passwords: list[PasswordInformation]) -> None:
        parent_beg = parent().getbegyx()
        self.pad_beg = parent_beg[0] + 3, parent_beg[1] + 1
        self.parent_max = parent().getmaxyx()
        self.pad_end = self.parent_max[0] + 5, self.parent_max[1] - 1

        if len(passwords) > 0:
            pad_height = len(passwords)
        else:
            pad_height = 1
        pad_width = self.pad_end[1] - 1

        self.pad = curses.newpad(pad_height, pad_width)
        self.position = 0
        self.selected = 0

        self.items: list[ListItem] = []

        for i, password in enumerate(passwords):
            self.items.append(
                ListItem(password,
                         i,
                         self.calculate_columns(self.parent_max[1]),
                         self)
            )

        if len(self.items) > 0:
            self.items[0].select()
        self.refresh()

    def add_item(self, password: PasswordInformation) -> None:
        size = self.pad_end[0] - self.pad_beg[0], self.pad_end[1] - \
               self.pad_beg[1]
        self.pad.resize(size[0] + 50, size[1])
        self.items.append(
            ListItem(
                password,
                len(self.items),
                self.calculate_columns(self.parent_max[1]),
                self,
            )
        )
        self.selected = len(self.items) - 1
        self.position = len(self.items)
        self.scroll_down()
        self.refresh()
        self.refresh_selected()

    def refresh(self) -> None:
        self.pad.refresh(
            self.position,
            0,
            self.pad_beg[0],
            self.pad_beg[1],
            self.pad_end[0],
            self.pad_end[1],
        )

    def select_next(self) -> None:
        if len(self.items) == 0:
            return
        self.items[self.selected].deselect()
        if self.selected >= len(self.items) - 1:
            self.selected = len(self.items) - 1
        else:
            self.selected += 1

        self.items[self.selected].select()

        if self.selected <= len(self.items) - 4:
            if self.selected > self.position + self.pad_end[0] - self.pad_beg[
                0] - 3:
                self.scroll_down()

        self.refresh()

    def select_previous(self) -> None:
        if len(self.items) == 0:
            return
        self.items[self.selected].deselect()
        if self.selected <= 0:
            self.selected = 0
        else:
            self.selected -= 1

        self.items[self.selected].select()

        if self.selected <= self.position + 2:
            self.scroll_up()
        self.refresh()

    def scroll_down(self) -> None:
        if self.position >= self.pad_end[0] - self.pad_beg[0]:
            self.position = self.pad_end[0] - self.pad_beg[0]
        else:
            self.position += 1
        self.refresh()

    def scroll_up(self) -> None:
        if self.position <= 0:
            self.position = 0
        else:
            self.position -= 1
        self.refresh()

    def toggle_selected(self) -> None:
        selected_item = self.items[self.selected]
        selected_item.showing_pass = not selected_item.showing_pass
        selected_item.select()
        self.refresh()

    def get_selected(self) -> PasswordInformation:
        return self.items[self.selected].password

    def refresh_selected(self) -> None:
        if len(self.items) > 0:
            self.items[self.selected].select()

    async def check_selected(self) -> None:
        await self.items[self.selected].display_status()
        self.refresh()

    async def check_all(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(item.display_status()) for item in
                     self.items]
            await asyncio.gather(*tasks)
        self.refresh()

    @staticmethod
    def calculate_columns(parent_max_x: int) -> tuple[int, int, int, int]:
        col_1 = percentage_of(35, parent_max_x - 2)
        col_2 = percentage_of(20, parent_max_x - 2)
        col_3 = percentage_of(35, parent_max_x - 2)
        col_4 = percentage_of(10, parent_max_x - 2)
        return col_1, col_2, col_3, col_4


class ListItem:
    def __init__(
            self,
            password: PasswordInformation,
            position: int,
            column_width: tuple[int, int, int, int],
            parent_list: PasswordList,
    ) -> None:
        self.pad = parent_list.pad
        self.position = position
        self.password = password
        self.col_width = column_width
        self.pass_list = parent_list
        self.showing_pass = False
        self.display_description()
        self.display_username()
        self.display_password()
        self.pad.addstr(
            self.position,
            self.col_width[0] + self.col_width[1] + self.col_width[2] + 1,
            "?",
        )

    def display_description(self, attr: int = 0) -> None:
        description = self.password.description.decode()
        if len(description) > self.col_width[0]:
            description = shorten_str(description, self.col_width[0])
        description = pad_with(description, self.col_width[2])
        self.pad.addstr(self.position, 0, description, attr)

    def display_username(self, attr: int = 0) -> None:
        username_bytes = self.password.details.username
        username = "-"
        if username_bytes is not None:
            username = username_bytes.decode()
        if len(username) > self.col_width[0]:
            username = shorten_str(username, self.col_width[1])
        username = pad_with(username, self.col_width[0])
        self.pad.addstr(self.position, self.col_width[0], username, attr)

    def display_password(self, attr: int = 0) -> None:
        password = 10 * "*"
        if self.showing_pass:
            self.password.decrypt_passwords()
            password = self.password.passwords[-1].password_bytes.decode()
            if len(password) > self.col_width[2]:
                password = shorten_str(password, self.col_width[2])

        password = pad_with(password, self.col_width[2])
        self.pad.addstr(
            self.position, self.col_width[0] + self.col_width[1], password, attr
        )

    async def display_status(self) -> None:
        status_col = self.col_width[0] + self.col_width[1] + self.col_width[
            2] + 1
        self.pad.addstr(self.position, status_col, "⧖", curses.color_pair(3))

        occurences = await self.password.check_pwned_status()

        if occurences == 0:
            self.pad.addstr(self.position,
                            status_col,
                            "✓",
                            curses.color_pair(3))
        else:
            self.pad.addstr(
                self.position,
                status_col,
                f"⚠ {occurences}",
                curses.color_pair(2)
            )

    def select(self) -> None:
        self.display_description(curses.A_REVERSE)
        self.display_username(curses.A_REVERSE)
        self.display_password(curses.A_REVERSE)

    def deselect(self) -> None:
        self.display_description()
        self.display_username()
        self.display_password()
