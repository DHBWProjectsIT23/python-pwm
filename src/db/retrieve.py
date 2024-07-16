import sqlite3

from src.model.user import User
from src.model.password import Password
from src.crypto.hashing import hash_sha256


def retrieve_user_by_hash(cursor: sqlite3.Cursor, username_hash: bytes) -> User:
    cursor.execute("SELECT * FROM users WHERE username=?", (username_hash,))
    user: list[tuple[bytes, Password]] = cursor.fetchall()
    if user is None:
        raise ValueError("User not found")
    if len(user) != 1:
        raise ValueError("Multiple users found")

    return User(user[0][0], user[0][1])


def retrieve_user_by_name(cursor: sqlite3.Cursor, username: str) -> User:
    return retrieve_user_by_hash(cursor, hash_sha256(username.encode()))
