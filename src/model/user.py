"""
Represents a user with hashed username and password, 
supporting plaintext password retrieval, setting, and checking, 
while ensuring the password is a master password.
"""
from __future__ import annotations

import os
from typing import Optional

from src.crypto.hashing import hash_sha256
from src.model.password import Password


class User:
    """
    A class representing a user with a hashed username and a password.

    Attributes:
        username (bytes): The hashed username of the user.
        password (Password): The Password instance associated with the user.
        iv (bytes): Initialization vector used for encryption.
        _clear_password (Optional[str]): The plaintext password of the user, if set.
        _clear_username (Optional[str]): The plaintext username of the user, if set.
    """
    def __init__(
        self,
        hashed_username: bytes,
        password: Password,
    ):
        """
        Initializes a new User instance.

        Args:
            hashed_username (bytes): The hashed username of the user.
            password (Password): The Password instance for the user.

        Raises:
            ValueError: If the provided password is not a master password.
        """
        self.username = hashed_username
        self.password = password
        self.iv = os.urandom(16)
        self._clear_password: Optional[str] = None
        self._clear_username: Optional[str] = None
        if not password.is_master:
            password.make_master()

    def set_clear_password(self, password: str) -> None:
        """
        Sets the plaintext password for the user.

        Args:
            password (str): The plaintext password to set.
        """
        self._clear_password = password

    def get_clear_password(self) -> str:
        """
        Retrieves the plaintext password for the user.

        Returns:
            str: The plaintext password.

        Raises:
            ValueError: If the plaintext password has not been set.
        """
        if self._clear_password is None:
            raise ValueError("Clear password not set")

        return self._clear_password

    def set_clear_username(self, username: str) -> None:
        """
        Sets the plaintext username for the user.

        Args:
            username (str): The plaintext username to set.
        """
        self._clear_username = username

    def get_clear_username(self) -> str:
        """
        Retrieves the plaintext username for the user.

        Returns:
            str: The plaintext username.

        Raises:
            ValueError: If the plaintext username has not been set.
        """
        if self._clear_username is None:
            raise ValueError("Clear password not set")

        return self._clear_username

    def has_clear_password(self) -> bool:
        """
        Checks if the plaintext password has been set.

        Returns:
            bool: True if the plaintext password is set, False otherwise.
        """
        return self._clear_password is not None

    def has_clear_username(self) -> bool:
        """
        Checks if the plaintext username has been set.

        Returns:
            bool: True if the plaintext username is set, False otherwise.
        """
        return self._clear_username is not None

    @staticmethod
    def new(username: str, password: str) -> User:
        """
        Creates a new User instance with the given username and password.

        Args:
            username (str): The plaintext username of the user.
            password (str): The plaintext password of the user.

        Returns:
            User: The newly created User instance.
        """
        return User(hash_sha256(username.encode()), Password(password))
