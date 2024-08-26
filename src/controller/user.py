"""
Provides database operations for managing user authentication and account data.
"""
import sqlite3
from typing import Optional
from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.user import User


def validate_login(cursor: sqlite3.Cursor, username: str, password: str) -> bool:
    """
    Validates the login credentials of a user by checking the provided
    username and password.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL queries.
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.

    Returns:
        bool: True if the credentials are valid (username and password match), False otherwise.
    """
    return validate_login_hashed(cursor, hash_sha256(username.encode()), password)


def validate_login_hashed(
    cursor: sqlite3.Cursor, username: bytes, password: str
) -> bool:
    """
    Validates the login credentials of a user by checking the provided
    hashed username and password.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL queries.
        username (bytes): The hashed username of the user attempting to log in.
        password (str): The password of the user attempting to log in.

    Returns:
        bool: True if the credentials are valid (hashed password matches), False otherwise.

    Raises:
        ValueError: If no user is found or multiple users are found with the given hashed username.
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
    Checks if a given username is unique in the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL queries.
        username (str): The username to check for uniqueness.

    Returns:
        bool: True if the username is unique (not already in use), False otherwise.
    """
    cursor.execute(
        """
    SELECT COUNT(username) FROM users WHERE username = ?
    """,
        (hash_sha256(username.encode()),),
    )
    result: list[tuple[int]] = cursor.fetchall()
    return result[0][0] == 0


def retrieve_user_by_hash(cursor: sqlite3.Cursor, username_hash: bytes) -> User:
    """
    Retrieves a user from the database using the hashed username.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL queries.
        username_hash (bytes): The hashed username of the user to retrieve.

    Returns:
        User: The `User` object corresponding to the given hashed username.

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
    """
    Deletes a specific user from the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL commands.
        user (User): The `User` object representing the user to be deleted.

    Returns:
        None
    """
    cursor.execute(
        """
        DELETE FROM users WHERE username=?
        """,
        (user.username,),
    )


def retrieve_user_by_name(cursor: sqlite3.Cursor, username: str) -> User:
    """
    Retrieves a user from the database using the username.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL queries.
        username (str): The username of the user to retrieve.

    Returns:
        User: The `User` object corresponding to the given username.
    """
    return retrieve_user_by_hash(cursor, hash_sha256(username.encode()))


def update_user(
    cursor: sqlite3.Cursor, user: User, old_username: Optional[bytes] = None
) -> None:
    """
    Updates the username and/or password of an existing user in the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL commands.
        user (User): The `User` object with updated information.
        old_username (Optional[bytes]): 
        The previous username of the user, if it needs to be updated.
    """
    if old_username is None:
        old_username = user.username
    cursor.execute(
        """
        UPDATE users
        SET username = ?,
            password = ?
        WHERE username = ?
        """,
        (user.username, user.password, old_username),
    )


def insert_user(cursor: sqlite3.Cursor, user: User) -> User:
    """
    Inserts a new user into the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used to execute SQL commands.
        user (User): The `User` object to be inserted.

    Returns:
        User: The inserted `User` object with its ID.

    Raises:
        ValueError: If the insertion fails or no user is inserted.
    """
    cursor.execute(
        """
        INSERT INTO users (username, password) VALUES(?, ?) RETURNING *
        """,
        (user.username, user.password),
    )
    inserted_user: list[tuple[bytes, Password]] = cursor.fetchall()

    if len(inserted_user) == 0:
        raise ValueError("Failed to insert user")

    return User(inserted_user[0][0], inserted_user[0][1])
