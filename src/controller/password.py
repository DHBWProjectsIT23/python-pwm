import pickle
import sqlite3
from typing import Optional

from src.crypto.fernet import decrypt_fernet
from src.crypto.key_derivation import scrypt_derive
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

    Returns: list[PasswordInformation]: A list of PasswordInformation objects
    for the given user.
    """
    cursor.execute(
        """
        SELECT id, description, username, passwords, categories, note, metadata, salt
        FROM passwords WHERE user=?
        """,
        (user.username,),
    )
    results: list[tuple[int, bytes, bytes, bytes, bytes, bytes, bytes, bytes]] = (
        cursor.fetchall()
    )

    password_informations: list[PasswordInformation] = []
    for result in results:
        password_id: int = result[0]
        description: bytes = result[1]
        username: Optional[bytes] = pickle.loads(result[2])
        passwords: list[Password] = pickle.loads(result[3])
        categories: list[bytes] = pickle.loads(result[4])
        note: Optional[bytes] = pickle.loads(result[5])
        metadata: EncryptedMetadata = pickle.loads(result[6])
        salt: bytes = pickle.loads(result[7])

        pw_info = PasswordInformation.from_db(
            salt,
            (description, username, categories, note),
            passwords,
            user,
        )
        pw_info.id = password_id
        pw_info.metadata = metadata
        pw_info.decrypt_data()
        password_informations.append(pw_info)

    return password_informations


def update_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation
) -> None:
    """
    Updates existing password information in the database.

    Args: cursor (sqlite3.Cursor): The SQLite cursor object.
    password_information (PasswordInformation): The updated
    PasswordInformation object.

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
            metadata = ?,
            salt = ?
        WHERE id = ?
        """,
        (
            password_information.details.description,
            pickle.dumps(password_information.details.username),
            pickle.dumps(password_information.passwords),
            pickle.dumps(password_information.details.categories),
            pickle.dumps(password_information.details.note),
            password_information.user.username,
            pickle.dumps(password_information.metadata),
            pickle.dumps(password_information.get_salt()),
            password_information.id,
        ),
    )


def validate_unique_password(
    cursor: sqlite3.Cursor, description: str, username: Optional[str], user: User
) -> bool:
    """
    Validates that a password with the given description and username is
    unique for the user.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
        description (str): The description of the password.
        username (Optional[str]): The username associated with the password.
        user (User): The user who owns the password information.

    Returns:
        bool: True if the password is unique, False otherwise.
    """
    cursor.execute(
        """
        SELECT description, username, salt FROM passwords
        WHERE user = ?
        """,
        (user.username,),
    )
    results: list[tuple[bytes, bytes, bytes]] = cursor.fetchall()
    for result in results:
        salt: bytes = pickle.loads(result[2])
        key, _ = scrypt_derive(user.get_clear_password().encode(), salt)
        desc: bytes = decrypt_fernet(result[0], key)
        uname: Optional[bytes] = pickle.loads(result[1])
        uname = decrypt_fernet(uname, key) if uname else None

        username_bytes = username.encode() if username is not None else None

        if desc == description.encode() and uname == username_bytes:
            return False

    return True


def delete_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation
) -> None:
    cursor.execute(
        """
        DELETE FROM passwords WHERE id=?
        """,
        (password_information.id,),
    )


def delete_password_information_of_user(cursor: sqlite3.Cursor, user: User) -> None:
    cursor.execute(
        """
        DELETE FROM passwords WHERE user=?
        """,
        (user.username,),
    )


def insert_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation
) -> PasswordInformation:
    """
    Inserts new password information into the database.

    Args: cursor (sqlite3.Cursor): The SQLite cursor object.
    password_information (PasswordInformation): The PasswordInformation
    object to insert.

    Returns: PasswordInformation: The inserted PasswordInformation object
    with the new ID.
    """
    if not password_information.data_is_encrypted:
        password_information.encrypt_data()

    password_information.encrypt_passwords()

    cursor.execute(
        """
        INSERT INTO passwords(
            description, username, passwords, categories, note, user, metadata, salt
        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """,
        (
            password_information.details.description,
            pickle.dumps(password_information.details.username),
            pickle.dumps(password_information.passwords),
            pickle.dumps(password_information.details.categories),
            pickle.dumps(password_information.details.note),
            password_information.user.username,
            pickle.dumps(password_information.metadata),
            pickle.dumps(password_information.get_salt()),
        ),
    )
    result: list[tuple[int]] = cursor.fetchall()
    password_information.id = result[0][0]
    return password_information
