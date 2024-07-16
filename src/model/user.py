from src.model.password import Password
from src.crypto.placeholder_2 import hash_sha256
import sqlite3


class User:
    def __init__(self, username: str, password: Password):
        self.username = hash_sha256(username.encode())
        self.password = password
        password.make_master()

    def safe_to_db(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute(
            """
            INSERT INTO users (username, password) VALUES(?, ?)
            """,
            (
                self.username,
                self.password.password,
            ),
        )
