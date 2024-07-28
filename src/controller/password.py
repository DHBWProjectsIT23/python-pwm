import sqlite3
from src.model.password_information import PasswordInformation
from src.model.password import PasswordList, convert_password_list


def retrieve_password_information(
    cursor: sqlite3.Cursor, user_hash: bytes
) -> list[PasswordInformation]:
    cursor.execute(
        "SELECT (password_information) FROM passwords WHERE user=?", (user_hash,)
    )
    rows: list[PasswordInformation] = cursor.fetchall()
    return [row[0] for row in rows]


def insert_password_information(
    cursor: sqlite3.Cursor, password_information: PasswordInformation
) -> None:
    cursor.execute(
        """
        INSERT INTO passwords(password_information, user) VALUES(?, ?)
        """,
        (password_information, password_information.user.username),
    )
