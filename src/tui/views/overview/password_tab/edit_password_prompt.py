import sqlite3
from typing import Optional

from src.controller.password import validate_unique_password
from src.model import password_information
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.panel import Panel
from src.tui.views.overview.password_tab.create_password_prompt import PasswordCreator

CONTROL_E = 5
MULTILINE_CTR_STR = "- ^G Continue -"
SINGLELINE_CTR_STR = "- ↩ Continue -"


class PasswordEditor(PasswordCreator):
    def __init__(self, parent: Panel, user: User, cursor: sqlite3.Cursor):
        super().__init__(parent, user, cursor)

    def run(
        self, passwordInformation: Optional[PasswordInformation] = None
    ) -> PasswordInformation:
        if passwordInformation is None:
            raise ValueError("PasswordInformation must be provided for editing")

        self.prompt = self.create_prompt_with_padding(self.parent)
        title = "Edit Password"

        initial_error = ""
        while True:
            description = self._enter_description(
                initial_error,
                password_information.description.decode(),
                title=title + " 2/2",
            )
            initial_username = (
                password_information.username.decode()
                if password_information.username
                else ""
            )
            username = self._enter_username(initial_username, title=title + " 3/3")

            if (
                description == password_information.description
                and username == password_information.username
            ):
                break

            if validate_unique_password(self.cursor, description, username, self.user):
                password_information.description = description.encode()
                password_information.username = username.encode()
                password_information.modify()
                break
            initial_error = "Identical combination already exists"

        categories = [category.decode() for category in password_information.categories]
        updated_categories = self._enter_categories(categories, title=title + " 5/5")
        if updated_categories != categories:
            password_information.categories = [
                category.encode() for category in updated_categories
            ]
            password_information.modify()

        updated_note = self._enter_note(password_information.note, title=title + " 6/6")
        note_bytes = updated_note.encode() if updated_note else None
        if note_bytes != password_information.note:
            password_information.note = note_bytes
            password_information.modify()

        self.prompt().clear()
        self.prompt().refresh()
        return password_information
