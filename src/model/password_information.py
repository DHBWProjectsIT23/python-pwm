from typing import Optional
from src.model.category import Category
from src.model.note import Note
from src.model.password import Password
from src.model.user import User


class PasswordInformation:
    def __init__(
        self,
        user: User,
        username: Optional[str] = None,
        email: Optional[str] = None,
        use_case: Optional[str] = None,
    ):
        self.passwords: list[Password] = []
        self.notes: list[Note] = []
        self.username: Optional[str] = username
        self.email: Optional[str] = email
        self.use_case: Optional[str] = use_case
        self.user: User = user
        self.categories: list[Category] = []

    def add_note(self, note: Note) -> None:
        self.notes.append(note)

    def add_password(self, password: Password) -> None:
        self.passwords.append(password)

    def add_category(self, category: Category) -> None:
        if len(self.categories) > 5:
            raise ValueError("Maximum of 5 categories allowed")
        if category in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(category)

    def encrypt(self, key: bytes) -> None:
        for password in self.passwords:
            password.encrypt(key)
        # TODO: Encrypt username, email, use_case, categories, notes

    def decrypt(self, key: bytes) -> None:
        for password in self.passwords:
            password.decrypt(key)
        # TODO: Decrypt username, email, use_case, categories, notes
