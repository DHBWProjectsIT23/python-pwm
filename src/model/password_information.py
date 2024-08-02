from typing import Iterable, Optional
import pickle
from src.model.password import Password
from src.model.user import User
from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet
from src.api.pawned import check_password


class PasswordInformation:
    def __init__(
        self,
        user: User,
        password: Password,
        description: str,
        username: Optional[str] = None,
    ):
        self.passwords: list[Password] = [password]
        self.description: Optional[str] = description
        self.username: Optional[str] = username
        self.categories: list[str] = []
        self.note: str = ""
        self.user: User = user
        self.is_encrypted = False

    def set_note(self, note: str) -> None:
        self.note = note

    def add_password(self, password: Password) -> None:
        self.passwords.append(password)

    def add_category(self, category: str) -> None:
        if len(self.categories) == 5:
            raise ValueError("Maximum of 5 categories allowed")
        if category in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(category)

    def add_categories(self, categories: Iterable[str]) -> None:
        if sum(1 for e in categories) + len(self.categories) > 5:
            raise ValueError("Maximum of 5 categories allowed")
        for category in categories:
            if self.categories.__contains__(category):
                raise ValueError("Category already exists")

        self.categories.extend(categories)

    def encrypt(self, key: bytes) -> None:
        for password in self.passwords:
            password.encrypt(key)
        self.is_encrypted = True
        # TODO: Encrypt username, email, use_case, categories, notes

    def decrypt(self, key: bytes) -> None:
        for password in self.passwords:
            password.decrypt(key)
        self.is_encrypted = False
        # TODO: Decrypt username, email, use_case, categories, notes

    async def check_pwned_status(self, key: bytes) -> int:
        latest_password = self.passwords[0]
        if latest_password.is_encrypted:
            latest_password.decrypt(key)
        return await check_password(latest_password.password)


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
