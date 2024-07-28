import sqlite3
from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.user import User


def validate_login(cursor: sqlite3.Cursor, username: str, password: str) -> bool:
    try:
        return (
            hash_sha256(password.encode())
            == retrieve_user_by_name(cursor, username).password()
        )
    except ValueError:
        return False


def retrieve_user_by_hash(cursor: sqlite3.Cursor, username_hash: bytes) -> User:
    cursor.execute("SELECT * FROM users WHERE username=?", (username_hash,))
    user: list[tuple[bytes, Password]] = cursor.fetchall()
    if len(user) == 0:
        raise ValueError("User not found")
    if len(user) > 1:
        raise ValueError("Multiple users found")

    return User(user[0][0], user[0][1])


def retrieve_user_by_name(cursor: sqlite3.Cursor, username: str) -> User:
    return retrieve_user_by_hash(cursor, hash_sha256(username.encode()))


def insert_user(cursor: sqlite3.Cursor, user: User) -> None:
    cursor.execute(
        """
        INSERT INTO users (username, password) VALUES(?, ?)
        """,
        (user.username, user.password),
    )
