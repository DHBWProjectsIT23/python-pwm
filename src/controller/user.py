import sqlite3
from typing import Optional
from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.user import User


def validate_login(cursor: sqlite3.Cursor, username: str, password: str) -> bool:
    """
    Validates the login credentials of a user by username and password.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    return validate_login_hashed(cursor, hash_sha256(username.encode()), password)


def validate_login_hashed(
    cursor: sqlite3.Cursor, username: bytes, password: str
) -> bool:
    """
    Validates the login credentials of a user by hashed username and password.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        username (bytes): The hashed username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    try:
        return (
            hash_sha256(password.encode())
            == retrieve_user_by_hash(cursor, username).password()
        )
    except ValueError:
        return False


def validate_unique_user(cursor: sqlite3.Cursor, username: str) -> bool:
    """
    Checks if a username is unique in the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        username (str): The username to check for uniqueness.

    Returns:
        bool: True if the username is unique, False otherwise.
    """
    cursor.execute(
        """
    SELECT COUNT(username) FROM users WHERE username = ?
    """,
        (hash_sha256(username.encode()),),
    )
    existing_users: int = cursor.fetchall()[0][0]
    return existing_users == 0


def retrieve_user_by_hash(cursor: sqlite3.Cursor, username_hash: bytes) -> User:
    """
    Retrieves a user from the database by hashed username.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        username_hash (bytes): The hashed username of the user.

    Returns:
        User: The User object corresponding to the hashed username.

    Raises:
        ValueError: If no user or multiple users are found with the given hashed username.
    """
    cursor.execute("SELECT * FROM users WHERE username=?", (username_hash,))
    user: list[tuple[bytes, Password]] = cursor.fetchall()
    if len(user) == 0:
        raise ValueError("User not found")
    if len(user) > 1:
        raise ValueError("Multiple users found")

    return User(user[0][0], user[0][1])


def delete_user(cursor: sqlite3.Cursor, user: User) -> None:
    cursor.execute(
        """
        DELETE FROM users WHERE username=?
        """,
        (user.username,),
    )


def retrieve_user_by_name(cursor: sqlite3.Cursor, username: str) -> User:
    """
    Retrieves a user from the database by username.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        username (str): The username of the user.

    Returns:
        User: The User object corresponding to the username.
    """
    return retrieve_user_by_hash(cursor, hash_sha256(username.encode()))


def update_user(
    cursor: sqlite3.Cursor, user: User, new_username: Optional[bytes] = None
) -> None:
    if new_username is None:
        new_username = user.username
    cursor.execute(
        """
        UPDATE users
        SET username = ?,
            password = ?
        WHERE username = ?
        """,
        (new_username, user.password, user.username),
    )


def insert_user(cursor: sqlite3.Cursor, user: User) -> User:
    """
    Inserts a new user into the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        user (User): The User object to be inserted.

    Returns:
        User: The inserted User object.

    Raises:
        ValueError: If the user insertion fails.
    """
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
