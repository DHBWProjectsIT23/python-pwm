import sqlite3

from src.model.user import User
from src.model.password import Password
from src.crypto.hashing import hash_sha256
from src.model.category import CategoryList


def retrieve_category_lists(cursor: sqlite3.Cursor) -> list[CategoryList]:
    cursor.execute("SELECT * FROM test_category")
    rows: list[tuple[int, CategoryList]] = cursor.fetchall()
    # Return the second column  of each row
    return [row[1] for row in rows]
