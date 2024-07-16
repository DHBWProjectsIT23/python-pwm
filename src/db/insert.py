import sqlite3

from src.model.user import User


def insert_user(cursor: sqlite3.Cursor, user: User) -> None:
    cursor.execute(
        """
        INSERT INTO users (username, password) VALUES(?, ?)
        """,
        (user.username, user.password),
    )
