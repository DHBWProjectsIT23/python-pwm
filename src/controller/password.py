from pickle import encode_long
import sqlite3
import json
from src.crypto.placeholder import dummy_encrypt_fernet
from src.model.password import Password, pickle
from src.model.password_information import (
    Optional,
    PasswordInformation,
    dummy_decrypt_fernet,
)
from src.model.user import User


def retrieve_password_information(
    cursor: sqlite3.Cursor, user: User
) -> list[PasswordInformation]:
    cursor.execute(
        """
        SELECT id, description, username, passwords, categories, note FROM passwords WHERE user=?
        """,
        (user.username,),
    )
    results: list[tuple[int, bytes, bytes, bytes, bytes, bytes]] = cursor.fetchall()

    password_informations: list[PasswordInformation] = []
    for result in results:
        id: int = result[0]
        description: bytes = result[1]
        username: Optional[bytes] = pickle.loads(result[2])
        passwords: list[Password] = pickle.loads(result[3])
        categories: list[bytes] = pickle.loads(result[4])
        note: Optional[bytes] = pickle.loads(result[5])

        password_informations.append(
            PasswordInformation.load_from_db(
                id, description, username, passwords, categories, note, user
            )
        )

    return password_informations


def update_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation, user: User
) -> None:
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
            note = ?
        WHERE id = ?
        """,
        (
            password_information.description,
            pickle.dumps(password_information.username),
            pickle.dumps(password_information.passwords),
            pickle.dumps(password_information.categories),
            pickle.dumps(password_information.note),
            password_information.id,
        ),
    )


def validate_unique_password(
    cursor: sqlite3.Cursor, description: str, username: Optional[str], user: User
) -> bool:
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

        if desc == description.encode() or uname == username_bytes:
            return False

    return True


def insert_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation
) -> PasswordInformation:
    if not password_information.data_is_encrypted:
        password_information.encrypt_data()

    password_information.encrypt_passwords()

    cursor.execute(
        """
        INSERT INTO passwords(
            description, username, passwords, categories, note, user
        ) VALUES(?, ?, ?, ?, ?, ?)
        RETURNING id
        """,
        (
            password_information.description,
            pickle.dumps(password_information.username),
            pickle.dumps(password_information.passwords),
            pickle.dumps(password_information.categories),
            pickle.dumps(password_information.note),
            password_information.user.username,
        ),
    )
    result: list[tuple[int]] = cursor.fetchall()
    password_information.set_id(result[0][0])
    return password_information
