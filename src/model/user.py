import sqlite3

from src.crypto.hashing import hash_sha256
from src.model.password import Password


class User:
    def __init__(self, hashed_username: bytes, password: Password):
        self.username = hashed_username
        self.password = password
        if not password.is_master:
            password.make_master()
