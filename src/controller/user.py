import sqlite3
from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.user import User


def validate_login(cursor: sqlite3.Cursor, username: str, password: str) -> bool:
    return validate_login_hashed(cursor, hash_sha256(username.encode()), password)


def validate_login_hashed(
    cursor: sqlite3.Cursor, username: bytes, password: str
) -> bool:
    try:
        return (
            hash_sha256(password.encode())
            == retrieve_user_by_hash(cursor, username).password()
        )
    except ValueError:
        return False


def validate_unique_user(cursor: sqlite3.Cursor, username: str) -> bool:
    cursor.execute(
        """
    SELECT COUNT(username) FROM users WHERE username = ?
    """,
        (hash_sha256(username.encode()),),
    )
    existing_users = cursor.fetchall()[0][0]
    return existing_users == 0


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


def insert_user(cursor: sqlite3.Cursor, user: User) -> User:
    cursor.execute(
        """
        INSERT INTO users (username, password) VALUES(?, ?) RETURNING *
        """,
        (user.username, user.password),
    )
    user: list[tuple[bytes, Password]] = cursor.fetchall()

    if len(user) == 0:
        raise ValueError("Failed to insert user")

    return User(user[0][0], user[0][1])
