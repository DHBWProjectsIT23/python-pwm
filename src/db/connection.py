import sqlite3

from src.model.password import Password, convert_password, adapt_password
from src.model.metadata import Metadata


def connect_to_db(db_path: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    initialize_tables(cursor)

    return connection, cursor


def initialize_tables(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY,
        data BLOB NOT NULL,
        user BLOB NOT NULL,
        FOREIGN KEY(user) REFERENCES users(user)
    );
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username BLOB UNIQUE NOT NULL,
        password password NOT NULL
    );
    """)
