# TODO: Docstring
import sqlite3

from src.config import db_path


def connect_to_db() -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database and initializes the
    necessary tables.

    Returns:
        sqlite3.Connection: The SQLite connection object.
    """
    connection = sqlite3.connect(db_path(),
                                 detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    initialize_tables(cursor)

    return connection


def initialize_tables(cursor: sqlite3.Cursor) -> None:
    """
    Initializes the necessary tables in the SQLite database if they do not
    already exist.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.

    Returns:
        None
    """
    cursor.execute(
        """
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
        """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        username BLOB UNIQUE NOT NULL,
        password password NOT NULL
    );
    """
    )
