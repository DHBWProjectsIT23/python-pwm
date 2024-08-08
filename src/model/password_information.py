from __future__ import annotations

from datetime import datetime
from typing import Callable
from typing import Iterable
from typing import Optional

from src.api.pawned import check_password
from src.crypto.fernet import decrypt_fernet
from src.crypto.fernet import encrypt_fernet
from src.crypto.key_derivation import scrypt_derive
from src.exceptions.encryption_exception import EncryptionException
from src.import_export.password_dict import PasswordInformationDict
from src.model.metadata import EncryptedMetadata
from src.model.metadata import Metadata
from src.model.password import Password
from src.model.user import User


class PasswordInformation:
    """
    A class to store and manage information related to a password.

    Attributes:
        user (User): The user associated with this password information.
        passwords (list[Password]): A list of passwords related to this information.
        description (bytes): A description of the password information.
        details (PasswordDetails): Details about the password information.
        metadata (Metadata | EncryptedMetadata): Metadata about the password information.
        data_is_encrypted (bool): Flag indicating whether the data is encrypted.
        id (Optional[int]): An optional identifier for the password information.
    """

    def __init__(
        self,
        user: User,
        password: Password,
        description: str,
        username: Optional[str] = None,
    ):
        """
        Initializes PasswordInformation with given details.

        Args:
            user (User): The user associated with this password information.
            password (Password): The initial password.
            description (str): A description of the password information.
            username (Optional[str]): The username associated with the password, if any.
        """
        self.passwords: list[Password] = [password]
        username_bytes: Optional[bytes] = (
            username.encode() if username is not None else None
        )
        self.details = PasswordDetails(description.encode(), username_bytes, [], None)
        self.user: User = user
        self.metadata: Metadata | EncryptedMetadata = Metadata()
        self._salt: Optional[bytes]
        self.data_is_encrypted = False
        self.id: Optional[int] = None

    def set_note(self, note: str) -> None:
        """
        Sets or updates the note associated with this password information.

        Args:
            note (str): The note to be added.

        Raises:
            EncryptionException: If data is encrypted, updating the note is not allowed.
        """
        if self.data_is_encrypted:
            raise EncryptionException("Can't add note while encrypted")
        self.details.note = note.encode()
        self.metadata.modify()

    def add_password(self, password: Password) -> None:
        """
        Adds a new password to the list of passwords.

        Args:
            password (Password): The password to be added.

        Raises:
            EncryptionException: If data is encrypted, adding a password is not allowed.
        """
        if self.data_is_encrypted:
            raise EncryptionException("Can't add password while encrypted")
        self.passwords.append(password)
        self.metadata.modify()

    def add_category(self, category: str) -> None:
        """
        Adds a single category to the list of categories.

        Args:
            category (str): The category to be added.

        Raises:
            EncryptionException: If data is encrypted, adding a category is not allowed.
            ValueError: If the maximum number of categories is reached or if the category already exists.
        """
        if self.data_is_encrypted:
            raise EncryptionException("Can't add category while encrypted")
        if len(self.details.categories) == 5:
            raise ValueError("Maximum of 5 categories allowed")
        if category.encode() in self.details.categories:
            raise ValueError("Category already exists")
        self.details.categories.append(category.encode())
        self.metadata.modify()

    def add_categories(self, categories: Iterable[str]) -> None:
        """
        Adds multiple categories to the list of categories.

        Args:
            categories (Iterable[str]): An iterable of categories to be added.

        Raises:
            EncryptionException: If data is encrypted, adding categories is not allowed.
            ValueError: If the total number of categories exceeds the limit or if any category already exists.
        """
        if self.data_is_encrypted:
            raise EncryptionException("Can't add categories while encrypted")
        if sum(1 for _ in categories) + len(self.details.categories) > 5:
            raise ValueError("Maximum of 5 categories allowed")
        for category in categories:
            if category.encode() in self.details.categories:
                raise ValueError("Category already exists")

        self.details.categories.extend([category.encode() for category in categories])
        self.metadata.modify()

    def modify(self) -> None:
        """
        Updates the metadata last modified timestamp.
        """
        self.metadata.modify()

    def encrypt_data(self, *, user_password: Optional[str] = None) -> None:
        """
        Encrypts the data using the provided key.

        Args:
            key (Optional[str]): The encryption key. If not provided, the user's
            clear password is used.

        Raises:
            EncryptionException: If metadata is already encrypted.
        """
        if user_password is None:
            user_password = self.user.get_clear_password()

        if isinstance(self.metadata, EncryptedMetadata):
            raise EncryptionException("Metadata is already encrypted")

        key, self._salt = scrypt_derive(user_password.encode())

        self.metadata = self.metadata.encrypt(key)
        self.details.encrypt(key)

        self.data_is_encrypted = True

    def decrypt_data(self, *, user_password: Optional[str] = None) -> None:
        """
        Decrypts the data using the provided key.

        Args:
            user_password (Optional[str]): The decryption key. If not provided, the user's clear password is used.

        Raises:
            EncryptionException: If metadata is not encrypted or if salt is missing.
        """
        if self._salt is None:
            raise EncryptionException("No Salt found")
        if user_password is None:
            user_password = self.user.get_clear_password()
        if isinstance(self.metadata, Metadata):
            raise EncryptionException("Metadata is not encrypted")

        key, _ = scrypt_derive(user_password.encode(), self._salt)

        self.metadata = self.metadata.decrypt(key)
        self.details.decrypt(key)

        self.data_is_encrypted = False

    def encrypt_passwords(self, *, user_password: Optional[str] = None) -> None:
        """
        Encrypts the passwords using the provided key.

        Args:
            user_password (Optional[str]): The encryption key. If not provided, the user's clear password is used.
        """
        if user_password is None:
            user_password = self.user.get_clear_password()

        for password in self.passwords:
            password.encrypt(user_password)

    def decrypt_passwords(self, *, user_password: Optional[str] = None) -> None:
        """
        Decrypts the passwords using the provided key.

        Args:
            user_password (Optional[str]): The decryption key. If not provided, the user's clear password is used.
        """
        if user_password is None:
            user_password = self.user.get_clear_password()

        for password in self.passwords:
            password.decrypt(user_password)

    def get_salt(self) -> bytes:
        """
        Retrieves the salt used for encryption.

        Returns:
            bytes: The salt used for encryption.

        Raises:
            ValueError: If the salt is not found.
        """
        if self._salt is None:
            raise ValueError("Salt not found")
        return self._salt

    async def check_pwned_status(self, *, user_password: Optional[str] = None) -> int:
        """
        Checks if the latest password has been compromised in a known data breach.

        Args:
            user_password (Optional[str]): The decryption key. If not provided, the user's clear password is used.

        Returns:
            int: The number of times the password has been found in a breach.
        """
        if user_password is None:
            user_password = self.user.get_clear_password()

        latest_password = self.passwords[-1]
        if latest_password.is_encrypted:
            latest_password.decrypt(user_password)
        return await check_password(latest_password.password_bytes)

    def to_dict(self) -> PasswordInformationDict:
        """
        Converts the PasswordInformation instance to a dictionary.

        Returns:
            PasswordInformationDict: A dictionary representation of the PasswordInformation instance.

        Raises:
            EncryptionException: If metadata is encrypted, decryption is required before conversion.
        """
        if self.data_is_encrypted:
            self.decrypt_data()
        self.decrypt_passwords()

        if not isinstance(self.metadata, Metadata):
            raise EncryptionException("Can't convert to dict if metadata is encrypted")

        return {
            "description": self.details.description.decode(),
            "username": self.details.username.decode() if self.details.username else "",
            "password": {
                "current_password": self.passwords[-1].password_bytes.decode(),
                "old_passwords": [
                    password.password_bytes.decode() for password in self.passwords[:-1]
                ],
            },
            "categories": [category.decode() for category in self.details.categories],
            "note": self.details.note.decode() if self.details.note else "",
            "created_at": self.metadata.created_at.timestamp(),
            "last_modified": self.metadata.last_modified.timestamp(),
        }

    @classmethod
    def from_dict(
        cls, data: PasswordInformationDict, user: User
    ) -> PasswordInformation:
        """
        Creates a PasswordInformation instance from a dictionary.

        Args:
            data (PasswordInformationDict): The dictionary containing password information.
            user (User): The user associated with this password information.

        Returns:
            PasswordInformation: An instance of PasswordInformation initialized with the data from the dictionary.
        """
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

        username: Optional[str] = data.get("username", None)
        password_information.details.username = username.encode() if username else None

        categories = data.get("categories", [])
        if len(categories) > 0:
            password_information.details.categories = [
                category.encode() for category in categories
            ]

        note = data.get("note", None)
        password_information.details.note = note.encode() if note else None

        return password_information

    @classmethod
    def from_db(
        cls,
        salt: bytes,
        details: tuple[bytes, Optional[bytes], list[bytes], Optional[bytes]],
        passwords: list[Password],
        user: User,
    ) -> PasswordInformation:
        """
        Creates a PasswordInformation instance from database values.

        Args:
            salt (bytes): The salt used for encryption.
            details (tuple[bytes, Optional[bytes], list[bytes], Optional[bytes]]): The details about the password information.
            passwords (list[Password]): The list of passwords.
            user (User): The user associated with this password information.

        Returns:
            PasswordInformation: An instance of PasswordInformation initialized with the database values.
        """
        password_information = cls(user, passwords[0], "")
        password_information._salt = salt
        password_information.details.description = details[0]
        password_information.details.username = details[1]
        password_information.passwords = passwords
        password_information.details.categories = details[2]
        password_information.details.note = details[3]
        password_information.data_is_encrypted = True
        return password_information

    @staticmethod
    def create_password_filter(
        search_string: str,
    ) -> Callable[[PasswordInformation], bool]:
        """
        Creates a filter function to check if a PasswordInformation instance matches the search criteria.

        Args:
            search_string (str): The search string to filter by.

        Returns:
            Callable[[PasswordInformation], bool]: A function that takes a PasswordInformation instance and returns
            True if it matches the search criteria, otherwise False.
        """
        def filter_passwords(password: PasswordInformation) -> bool:
            if password.data_is_encrypted:
                raise EncryptionException("Data needs to be decrypted for searching")
            if search_string.lower() in password.details.description.decode().lower():
                return True
            for category in password.details.categories:
                if search_string.lower() in category.decode().lower():
                    return True
            return False

        return filter_passwords


class PasswordDetails:
    """
    A class to store details related to a password.

    Attributes:
        description (bytes): A description of the password details.
        username (Optional[bytes]): The username associated with the password.
        categories (list[bytes]): A list of categories for the password.
        note (Optional[bytes]): An optional note associated with the password.
    """
    def __init__(
        self,
        description: bytes,
        username: Optional[bytes],
        categories: list[bytes],
        note: Optional[bytes],
    ):
        """
        Initializes PasswordDetails with given details.

        Args:
            description (bytes): A description of the password details.
            username (Optional[bytes]): The username associated with the password.
            categories (list[bytes]): A list of categories for the password.
            note (Optional[bytes]): An optional note associated with the password.
        """
        self.description = description
        self.username = username
        self.categories = categories
        self.note = note

    def encrypt(self, key: bytes) -> None:
        """
        Encrypts the password details using the provided key.

        Args:
            key (bytes): The encryption key.
        """
        _ = key
        self.description = encrypt_fernet(self.description, key)
        if self.username is not None:
            self.username = encrypt_fernet(self.username, key)

        if self.note is not None:
            self.note = encrypt_fernet(self.note, key)

        self.categories = [
            encrypt_fernet(category, key) for category in self.categories
        ]

    def decrypt(self, key: bytes) -> None:
        """
        Decrypts the password details using the provided key.

        Args:
            key (bytes): The decryption key.
        """
        _ = key
        self.description = decrypt_fernet(self.description, key)
        if self.username is not None:
            self.username = decrypt_fernet(self.username, key)

        if self.note is not None:
            self.note = decrypt_fernet(self.note, key)

        self.categories = [
            decrypt_fernet(category, key) for category in self.categories
        ]
