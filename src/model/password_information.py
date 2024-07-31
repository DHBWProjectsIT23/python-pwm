from typing import Iterable, Optional, Type
import pickle
from src.model.category import Category, CategoryList
from src.model.note import Note, NoteList
from src.model.password import Password, PasswordList
from src.model.user import User
from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet


class PasswordInformation:
    def __init__(
        self,
        user: User,
        password: Password,
        description: str,
        username: Optional[str] = None,
    ):
        self.passwords: PasswordList = PasswordList([password])
        self.description: Optional[str] = description
        self.username: Optional[str] = username
        self.categories: CategoryList = CategoryList()
        self.notes: NoteList = NoteList()
        self.user: User = user

    def add_note(self, note: Note) -> None:
        self.notes.append(note)

    def add_password(self, password: Password) -> None:
        self.passwords.append(password)

    def add_category(self, category: Category) -> None:
        if len(self.categories) == 5:
            raise ValueError("Maximum of 5 categories allowed")
        if category in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(category)

    def add_categories(self, categories: Iterable[Category]) -> None:
        if sum(1 for e in categories) + len(self.categories) > 5:
            raise ValueError("Maximum of 5 categories allowed")
        for category in categories:
            if self.categories.__contains__(category):
                raise ValueError("Category already exists")

        self.categories.extend(categories)

    def encrypt(self, key: bytes) -> None:
        for password in self.passwords:
            password.encrypt(key)
        # TODO: Encrypt username, email, use_case, categories, notes

    def decrypt(self, key: bytes) -> None:
        for password in self.passwords:
            password.decrypt(key)
        # TODO: Decrypt username, email, use_case, categories, notes


def adapt_password_information(password_information: PasswordInformation) -> bytes:
    for password in password_information.passwords:
        if not password.is_encrypted:
            raise ValueError("Password is not encrypted")

        if password.is_master:
            raise TypeError("Can not store master password in password information")

    password_information_bytes = pickle.dumps(password_information)
    return dummy_encrypt_fernet(password_information_bytes)


def convert_password_information(password_information: bytes) -> PasswordInformation:
    password_information_bytes = dummy_decrypt_fernet(password_information)
    retrieved_password_information: PasswordInformation = pickle.loads(
        password_information_bytes
    )

    if not isinstance(retrieved_password_information, PasswordInformation):
        raise TypeError("PasswordInformation expected")

    return retrieved_password_information
