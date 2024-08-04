from __future__ import annotations

from typing import Optional

from src.crypto.hashing import hash_sha256
from src.model.metadata import Metadata
from src.model.password import Password


class User:
    def __init__(self, hashed_username: bytes, password: Password):
        self.username = hashed_username
        self.password = password
        self._clear_password: Optional[str] = None
        if not password.is_master:
            password.make_master()

    def set_clear_password(self, password: str) -> None:
        self._clear_password = password

    def get_clear_password(self) -> str:
        if self._clear_password is None:
            raise ValueError("Clear password not set")

        return self._clear_password

    def has_clear_password(self) -> bool:
        return self._clear_password is not None

    @staticmethod
    def new(username: str, password: str) -> User:
        return User(hash_sha256(username.encode()), Password(password, Metadata()))
