from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, Iterable, Optional  # noqa: F401
from src.import_export.password_dict import PasswordInformationDict

from src.api.pawned import check_password
from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet
from src.exceptions.encryption_exception import EncryptionException
from src.model.metadata import EncryptedMetadata, Metadata
from src.model.password import Password
from src.model.user import User


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
        self.metadata: Metadata | EncryptedMetadata = Metadata()
        self.data_is_encrypted = False
        self.id: Optional[int] = None

    def set_note(self, note: str) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add note while encrypted")
        self.note = note.encode()
        self.metadata.modify()

    def add_password(self, password: Password) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add password while encrypted")
        self.passwords.append(password)
        self.metadata.modify()

    def add_category(self, category: str) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add category while encrypted")
        if len(self.categories) == 5:
            raise ValueError("Maximum of 5 categories allowed")
        if category.encode() in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(category.encode())
        self.metadata.modify()

    def add_categories(self, categories: Iterable[str]) -> None:
        if self.data_is_encrypted:
            raise EncryptionException("Can't add categories while encrypted")
        if sum(1 for e in categories) + len(self.categories) > 5:
            raise ValueError("Maximum of 5 categories allowed")
        for category in categories:
            if self.categories.__contains__(category):
                raise ValueError("Category already exists")

        self.categories.extend([category.encode() for category in categories])
        self.metadata.modify()

    def modify(self) -> None:
        self.metadata.modify()

    def encrypt_data(self, *, key: Optional[str] = None) -> None:
        """
        FERNET
        """
        key_bytes = b""
        if key is None:
            key_bytes = self.user.get_clear_password().encode()
        else:
            key_bytes = key.encode()

        self.description = dummy_encrypt_fernet(self.description)

        if isinstance(self.metadata, EncryptedMetadata):
            raise EncryptionException("Metadata is already encrypted")

        self.metadata = self.metadata.encrypt(key_bytes)

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
        key_bytes = b""
        if key is None:
            key_bytes = self.user.get_clear_password().encode()
        else:
            key_bytes = key.encode()

        self.description = dummy_decrypt_fernet(self.description)

        if isinstance(self.metadata, Metadata):
            raise EncryptionException("Metadata is not encrypted")

        self.metadata = self.metadata.decrypt(key_bytes)

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
        key_bytes = b""
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
        key_bytes = b""
        if key is None:
            key = self.user.get_clear_password()

        for password in self.passwords:
            password.decrypt(key.encode())

    async def check_pwned_status(self, *, key: Optional[str] = None) -> int:
        if key is None:
            key = self.user.get_clear_password()

        latest_password = self.passwords[-1]
        if latest_password.is_encrypted:
            latest_password.decrypt(key.encode())
        return await check_password(latest_password.password)

    def to_dict(self) -> PasswordInformationDict:
        if self.data_is_encrypted:
            self.decrypt_data()
        self.decrypt_passwords()

        if not isinstance(self.metadata, Metadata):
            raise EncryptionException("Can't convert to dict if metadata is encrypted")

        return {
            "description": self.description.decode(),
            "username": self.username.decode() if self.username else "",
            "password": {
                "current_password": self.passwords[-1].password.decode(),
                "old_passwords": [
                    password.password.decode() for password in self.passwords[:-1]
                ],
            },
            "categories": [category.decode() for category in self.categories],
            "note": self.note.decode() if self.note else "",
            "created_at": self.metadata.created_at.timestamp(),
            "last_modified": self.metadata.last_modified.timestamp(),
        }

    @classmethod
    def from_dict(
        cls, data: PasswordInformationDict, user: User
    ) -> PasswordInformation:
        # Required Data
        description = data["description"]
        current_password = data["password"]["current_password"]
        passwords = data["password"].get("old_passwords", [])
        passwords.append(current_password)

        password_information = cls(user, Password("WILL_BE_CHANGED"), description)
        password_information.passwords = [Password(password) for password in passwords]

        # Optional Data
        metadata = Metadata()
        created_at = data.get("created_at", None)
        if created_at is not None:
            metadata.created_at = datetime.fromtimestamp(created_at)
        modified_at = data.get("last_modified", None)
        if modified_at is not None:
            metadata.last_modified = datetime.fromtimestamp(modified_at)
        password_information.metadata = metadata

        password_information.username = (
            data.get("username", None).encode() if data.get("username", None) else None
        )

        categories = data.get("categories", [])
        if len(categories) > 0:
            password_information.categories = [
                category.encode() for category in categories
            ]
        password_information.note = (
            data.get("note", None).encode() if data.get("note", None) else None
        )

        return password_information

    @classmethod
    def from_db(
        cls,
        id: int,
        description: bytes,
        username: Optional[bytes],
        passwords: list[Password],
        categories: list[bytes],
        note: Optional[bytes],
        user: User,
        metadata: EncryptedMetadata,
    ) -> PasswordInformation:
        password_information = cls(user, passwords[0], "")
        password_information.id = id
        password_information.description = description
        password_information.username = username
        password_information.passwords = passwords
        password_information.categories = categories
        password_information.note = note
        password_information.metadata = metadata
        password_information.data_is_encrypted = True
        password_information.decrypt_data()
        return password_information
