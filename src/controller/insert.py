import sqlite3

from src.model.user import User
from src.model.category import CategoryList


def insert_category_list(cursor: sqlite3.Cursor, category_list: CategoryList) -> None:
    cursor.execute(
        """
        INSERT INTO test_category (category_list) VALUES(?)
        """,
        (category_list,),
    )
