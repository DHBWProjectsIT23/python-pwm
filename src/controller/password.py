import pickle
import sqlite3
from typing import Optional
from src.crypto.placeholder import dummy_encrypt_fernet, dummy_decrypt_fernet
from src.model.metadata import EncryptedMetadata
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.user import User


def retrieve_password_information(
    cursor: sqlite3.Cursor, user: User
) -> list[PasswordInformation]:
    """
    Retrieves password information for a given user from the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        user (User): The user whose password information is to be retrieved.

    Returns:
        list[PasswordInformation]: A list of PasswordInformation objects for the given user.
    """
    cursor.execute(
        """
        SELECT id, description, username, passwords, categories, note, metadata FROM passwords WHERE user=?
        """,
        (user.username,),
    )
    results: list[tuple[int, bytes, bytes, bytes, bytes, bytes, bytes]] = (
        cursor.fetchall()
    )

    password_informations: list[PasswordInformation] = []
    for result in results:
        id: int = result[0]
        description: bytes = result[1]
        username: Optional[bytes] = pickle.loads(result[2])
        passwords: list[Password] = pickle.loads(result[3])
        categories: list[bytes] = pickle.loads(result[4])
        note: Optional[bytes] = pickle.loads(result[5])
        metadata: EncryptedMetadata = pickle.loads(result[6])

        password_informations.append(
            PasswordInformation.from_db(
                id, description, username, passwords, categories, note, user, metadata
            )
        )

    return password_informations


def update_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation, user: User
) -> None:
    """
    Updates existing password information in the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        password_information (PasswordInformation): The updated PasswordInformation object.
        user (User): The user who owns the password information.

    Returns:
        None
    """
    if not password_information.data_is_encrypted:
        password_information.encrypt_data()

    password_information.encrypt_passwords()

    cursor.execute(
        """
        UPDATE passwords
        SET description = ?,
            username = ?,
            passwords = ?,
            categories = ?,
            note = ?,
            user = ?,
            metadata = ?
        WHERE id = ?
        """,
        (
            password_information.description,
            pickle.dumps(password_information.username),
            pickle.dumps(password_information.passwords),
            pickle.dumps(password_information.categories),
            pickle.dumps(password_information.note),
            password_information.user.username,
            pickle.dumps(password_information.metadata),
            password_information.id,
        ),
    )


def validate_unique_password(
    cursor: sqlite3.Cursor, description: str, username: Optional[str], user: User
) -> bool:
    """
    Validates that a password with the given description and username is unique for the user.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        description (str): The description of the password.
        username (Optional[str]): The username associated with the password.
        user (User): The user who owns the password information.

    Returns:
        bool: True if the password is unique, False otherwise.
    """
    # TODO: Encrypt/Decrypt same as in PWInfo
    cursor.execute(
        """
        SELECT description, username FROM passwords
        WHERE user = ?
        """,
        (user.username,),
    )
    results: list[tuple[bytes, bytes]] = cursor.fetchall()
    for result in results:
        desc: bytes = dummy_decrypt_fernet(result[0])
        uname: Optional[bytes] = (
            dummy_decrypt_fernet(pickle.loads(result[1]))
            if pickle.loads(result[1]) is not None
            else None
        )

        username_bytes = username.encode() if username is not None else None

        if desc == description.encode() and uname == username_bytes:
            return False

    return True


def insert_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation
) -> PasswordInformation:
    """
    Inserts new password information into the database.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        password_information (PasswordInformation): The PasswordInformation object to insert.

    Returns:
        PasswordInformation: The inserted PasswordInformation object with the new ID.
    """
    if not password_information.data_is_encrypted:
        password_information.encrypt_data()

    password_information.encrypt_passwords()

    cursor.execute(
        """
        INSERT INTO passwords(
            description, username, passwords, categories, note, user, metadata
        ) VALUES(?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """,
        (
            password_information.description,
            pickle.dumps(password_information.username),
            pickle.dumps(password_information.passwords),
            pickle.dumps(password_information.categories),
            pickle.dumps(password_information.note),
            password_information.user.username,
            pickle.dumps(password_information.metadata),
        ),
    )
    result: list[tuple[int]] = cursor.fetchall()
    password_information.id = result[0][0]
    return password_information
