"""
Module for editing existing passwords in the terminal user interface.

This module provides functionality for prompting the user to edit an existing password, including
its description, username, categories, and note.
"""

import sqlite3
from typing import Optional

from src.controller.password import validate_unique_password
from src.exceptions.exit_from_textbox_exception import ExitFromTextBoxException
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.tui.panel import Panel
from src.tui.views.overview.password_tab.create_password_prompt import (
    PasswordCreationPrompt,
)

CONTROL_E = 5
MULTILINE_CTR_STR = "- ^G Continue -"
SINGLELINE_CTR_STR = "- ↩ Continue -"


class PasswordEditPrompt(PasswordCreationPrompt):
    """
    Class for the user prompt to edit an existing password.

    This class allows the user to edit details of an existing password, such as its description,
    username, categories, and note. It ensures that any updates are validated and saved correctly.
    """

    def __init__(
        self,
        parent: Panel,
        user: User,
        password_information: PasswordInformation,
        cursor: sqlite3.Cursor,
    ):
        """
        Initializes the PasswordEditPrompt class.

        Args:
            parent (Panel): The parent panel for the prompt.
            user (User): The current user.
            password_information (PasswordInformation):
            The existing password information to be edited.
            cursor (sqlite3.Cursor): The database cursor for database operations.
        """
        super().__init__(parent, user, cursor)
        self.password_information = password_information

    def run(self) -> Optional[PasswordInformation]:
        """
        Executes the prompt to edit an existing password.

        This method displays prompts to the user for editing the password's description, username,
        categories, and note. It ensures that the new details are valid and unique before updating
        the password information.

        Returns:
            Optional[PasswordInformation]: The updated password information if the operation was
            successful, otherwise None.
        """

        self.prompt = self.create_prompt_with_padding(self.parent)
        title = "Edit Password"

        try:
            initial_error = ""
            while True:
                description = self._enter_description(
                    initial_error,
                    self.password_information.details.description.decode(),
                    title=title + " 2/2",
                )
                initial_username = (
                    self.password_information.details.username.decode()
                    if self.password_information.details.username
                    else ""
                )
                username = self._enter_username(initial_username, title=title + " 3/3")
                old_username = (
                    self.password_information.details.username.decode()
                    if self.password_information.details.username
                    else None
                )
                if (
                    description.encode()
                    == self.password_information.details.description
                    and username == old_username
                ):
                    break

                if validate_unique_password(
                    self.cursor, description, username, self.user
                ):
                    self.password_information.details.description = description.encode()
                    self.password_information.details.username = (
                        username.encode() if username else None
                    )
                    self.password_information.modify()
                    break
                initial_error = "Identical combination already exists"

            categories = [
                category.decode()
                for category in self.password_information.details.categories
            ]
            updated_categories = self._enter_categories(
                categories, title=title + " 5/5"
            )
            if updated_categories != categories:
                self.password_information.details.categories = [
                    category.encode() for category in updated_categories
                ]
                self.password_information.modify()

            old_note = (
                self.password_information.details.note.decode()
                if self.password_information.details.note
                else None
            )
            updated_note = self._enter_note(old_note, title=title + " 6/6")
            note_bytes = updated_note.encode() if updated_note else None
            if note_bytes != self.password_information.details.note:
                self.password_information.details.note = note_bytes
                self.password_information.modify()

        except ExitFromTextBoxException:
            self.break_out()
            return None

        self.break_out()
        return self.password_information
