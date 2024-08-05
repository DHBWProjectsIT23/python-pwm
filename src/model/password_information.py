from __future__ import annotations
from typing import Iterable, Optional
from src.model.password import Password
from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet
from src.model.user import User
from src.exceptions.encryption_exception import EncryptionException
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
        self.description: bytes = description.encode()
        self.username: Optional[bytes] = (
            username.encode() if username is not None else None
        )
        self.categories: list[bytes] = []
        self.note: Optional[bytes] = None
        self.user: User = user
        self.data_is_encrypted = False
        self.id: Optional[int] = None

    def set_note(self, note: str) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add note while encrypted")
        self.note = note.encode()

    def add_password(self, password: Password) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add password while encrypted")
        self.passwords.append(password)

    def add_category(self, category: str) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add category while encrypted")
        if len(self.categories) == 5:
            raise ValueError("Maximum of 5 categories allowed")
        if category.encode() in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(category.encode())

    def add_categories(self, categories: Iterable[str]) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add categories while encrypted")
        if sum(1 for e in categories) + len(self.categories) > 5:
            raise ValueError("Maximum of 5 categories allowed")
        for category in categories:
            if self.categories.__contains__(category):
                raise ValueError("Category already exists")

        self.categories.extend([category.encode() for category in categories])

    def set_id(self, id: int) -> None:
        self.id = id

    def encrypt_data(self, *, key: Optional[str] = None) -> None:
        """
        FERNET
        """
        if key is None:
            key_bytes = self.user.get_clear_password().encode()
        else:
            key_bytes = key.encode()

        self.description = dummy_encrypt_fernet(self.description)

        if self.username is not None:
            self.username = dummy_encrypt_fernet(self.username)

        if self.note is not None:
            self.note = dummy_encrypt_fernet(self.note)

        if len(self.categories) > 0:
            self.categories = [
                dummy_encrypt_fernet(category) for category in self.categories
            ]

        self.data_is_encrypted = True

    def decrypt_data(self, *, key: Optional[str] = None) -> None:
        """
        FERNET
        """
        if key is None:
            key_bytes = self.user.get_clear_password().encode()
        else:
            key_bytes = key.encode()

        self.description = dummy_decrypt_fernet(self.description)

        if self.username is not None:
            self.username = dummy_decrypt_fernet(self.username)

        if self.note is not None:
            self.note = dummy_decrypt_fernet(self.note)

        if len(self.categories) > 0:
            self.categories = [
                dummy_decrypt_fernet(category) for category in self.categories
            ]

        self.data_is_encrypted = False

    def encrypt_passwords(self, *, key: Optional[str] = None) -> None:
        """
        AES256
        """
        if key is None:
            key_bytes = self.user.get_clear_password().encode()
        else:
            key_bytes = key.encode()

        for password in self.passwords:
            password.encrypt(key_bytes)

    def decrypt_passwords(self, *, key: Optional[str] = None) -> None:
        """
        AES256
        """
        if key is None:
            key = self.user.get_clear_password()

        for password in self.passwords:
            password.decrypt(key.encode())

    async def check_pwned_status(self, key: bytes) -> int:
        latest_password = self.passwords[0]
        if latest_password.is_encrypted:
            latest_password.decrypt(key)
        return await check_password(latest_password.password)

    @staticmethod
    def load_from_db(
        id: int,
        description: bytes,
        username: Optional[bytes],
        passwords: list[Password],
        categories: list[bytes],
        note: Optional[bytes],
        user: User,
    ) -> PasswordInformation:
        password_information = PasswordInformation(user, passwords[0], "")
        password_information.set_id(id)
        password_information.description = description
        password_information.username = username
        password_information.passwords = passwords
        password_information.categories = categories
        password_information.note = note
        password_information.data_is_encrypted = True
        password_information.decrypt_data()
        return password_information
