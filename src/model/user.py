from __future__ import annotations

from src.crypto.hashing import hash_sha256
from src.model.metadata import Metadata
from src.model.password import Password


class User:
    def __init__(self, hashed_username: bytes, password: Password):
        self.username = hashed_username
        self.password = password
        if not password.is_master:
            password.make_master()

    @staticmethod
    def new(username: str, password: str) -> User:
        return User(hash_sha256(username.encode()), Password(password, Metadata()))
