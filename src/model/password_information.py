from __future__ import annotations

from datetime import datetime
from typing import Callable
from typing import Iterable
from typing import Optional

from src.api.pawned import check_password
from src.crypto.placeholder import dummy_decrypt_fernet
from src.crypto.placeholder import dummy_encrypt_fernet
from src.exceptions.encryption_exception import EncryptionException
from src.import_export.password_dict import PasswordInformationDict
from src.model.metadata import EncryptedMetadata
from src.model.metadata import Metadata
from src.model.password import Password
from src.model.user import User


class PasswordInformation:
    """
    A class to store and manage information related to a password.

    Attributes: user (User): The user associated with this password
    information. passwords (list[Password]): A list of passwords related to
    this information. description (bytes): A description of the password
    information. details (PasswordDetails): Details about the password
    information. metadata (Metadata | EncryptedMetadata): Metadata about the
    password information. data_is_encrypted (bool): Flag indicating whether
    the data is encrypted. id (Optional[int]): An optional identifier for the
    password information.
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
            username (Optional[str]): The username associated with the password,
            if any.
        """
        self.passwords: list[Password] = [password]
        self.description: bytes = description.encode()
        username_bytes: Optional[bytes] = (
            username.encode() if username is not None else None
        )
        self.details = PasswordDetails(username_bytes, [], None)
        self.user: User = user
        self.metadata: Metadata | EncryptedMetadata = Metadata()
        self.data_is_encrypted = False
        self.id: Optional[int] = None

    def set_note(self, note: str) -> None:
        """
        Sets or updates the note associated with this password information.

        Args:
            note (str): The note to be added.

        Raises: EncryptionException: If data is encrypted, updating the note
        is not allowed.
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

        Raises: EncryptionException: If data is encrypted, adding a password
        is not allowed.
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
            EncryptionException: If data is encrypted, adding a category is not
            allowed.
            ValueError: If the maximum number of categories is reached or if the
            category already exists.
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
            EncryptionException: If data is encrypted, adding categories is not
            allowed.
            ValueError: If the total number of categories exceeds the limit or
            if any category already exists.
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

    def encrypt_data(self, *, key: Optional[str] = None) -> None:
        """
        Encrypts the data using the provided key.

        Args:
            key (Optional[str]): The encryption key. If not provided, the user's
            clear password is used.

        Raises:
            EncryptionException: If metadata is already encrypted.
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

        self.details.encrypt(key_bytes)

        self.data_is_encrypted = True

    def decrypt_data(self, *, key: Optional[str] = None) -> None:
        """
        Decrypts the data using the provided key.

        Args:
            key (Optional[str]): The decryption key. If not provided, the user's
            clear password is used.

        Raises:
            EncryptionException: If metadata is not encrypted.
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

        self.details.decrypt(key_bytes)

        self.data_is_encrypted = False

    def encrypt_passwords(self, *, key: Optional[str] = None) -> None:
        """
        Encrypts the passwords using the provided key.

        Args:
            key (Optional[str]): The encryption key. If not provided, the user's
            clear password is used.
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
        Decrypts the passwords using the provided key.

        Args:
            key (Optional[str]): The decryption key. If not provided, the user's
            clear password is used.
        """
        key_bytes = b""
        if key is None:
            key = self.user.get_clear_password()

        for password in self.passwords:
            password.decrypt(key.encode())

    async def check_pwned_status(self, *, key: Optional[str] = None) -> int:
        """
        Checks if the latest password has been compromised in a known data
        breach.

        Args:
            key (Optional[str]): The decryption key. If not provided, the user's
            clear password is used.

        Returns:
            int: The number of times the password has been found in a breach.
        """
        if key is None:
            key = self.user.get_clear_password()

        latest_password = self.passwords[-1]
        if latest_password.is_encrypted:
            latest_password.decrypt(key.encode())
        return await check_password(latest_password.password_bytes)

    def to_dict(self) -> PasswordInformationDict:
        """
        Converts the PasswordInformation instance to a dictionary.

        Returns:
            PasswordInformationDict: A dictionary representation of the
            PasswordInformation instance.

        Raises:
            EncryptionException: If metadata is encrypted, decryption is
            required before conversion.
        """
        if self.data_is_encrypted:
            self.decrypt_data()
        self.decrypt_passwords()

        if not isinstance(self.metadata, Metadata):
            raise EncryptionException("Can't convert to dict if metadata is encrypted")

        return {
            "description": self.description.decode(),
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
            data (PasswordInformationDict): The dictionary containing password
            information.
            user (User): The user associated with this password information.

        Returns:
            PasswordInformation: An instance of PasswordInformation initialized
            with the data from the dictionary.
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
        description: bytes,
        details: tuple[Optional[bytes], list[bytes], Optional[bytes]],
        passwords: list[Password],
        user: User,
    ) -> PasswordInformation:
        password_information = cls(user, passwords[0], "")
        password_information.description = description
        password_information.details.username = details[0]
        password_information.passwords = passwords
        password_information.details.categories = details[1]
        password_information.details.note = details[2]
        password_information.data_is_encrypted = True
        password_information.decrypt_data()
        return password_information

    @staticmethod
    def create_password_filter(
        search_string: str,
    ) -> Callable[[PasswordInformation], bool]:
        def filter_passwords(password: PasswordInformation) -> bool:
            if password.data_is_encrypted:
                raise EncryptionException("Data needs to be decrypted for searching")
            if search_string.lower() in password.description.decode().lower():
                return True
            for category in password.details.categories:
                if search_string.lower() in category.decode().lower():
                    return True
            return False

        return filter_passwords


class PasswordDetails:
    def __init__(
        self, username: Optional[bytes], categories: list[bytes], note: Optional[bytes]
    ):
        self.username = username
        self.categories = categories
        self.note = note

    def encrypt(self, key: bytes) -> None:
        if self.username is not None:
            self.username = dummy_encrypt_fernet(self.username)

        if self.note is not None:
            self.note = dummy_encrypt_fernet(self.note)

        self.categories = [
            dummy_encrypt_fernet(category) for category in self.categories
        ]

    def decrypt(self, key: bytes) -> None:
        if self.username is not None:
            self.username = dummy_decrypt_fernet(self.username)

        if self.note is not None:
            self.note = dummy_decrypt_fernet(self.note)

        self.categories = [
            dummy_decrypt_fernet(category) for category in self.categories
        ]
