import sqlite3

from src.crypto.hashing import hash_sha256
from src.db.retrieve import retrieve_user_by_name


def validate_login(cursor: sqlite3.Cursor, username: str, password: str) -> bool:
    try:
        return (
            hash_sha256(password.encode())
            == retrieve_user_by_name(cursor, username).password()
        )
    except ValueError:
        return False
