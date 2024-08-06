import sqlite3

DB_PATH: str = "test.db"


def connect_to_db(db_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    initialize_tables(cursor)

    return connection


def initialize_tables(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description BLOB NOT NULL,
        username BLOB,
        passwords BLOB NOT NULL,
        categories BLOB,
        note BLOB,
        user BLOB NOT NULL,
        metadata BLOB NOT NULL,
        FOREIGN KEY(user) REFERENCES users(username)
    );
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username BLOB UNIQUE NOT NULL,
        password password NOT NULL
    );
    """)
