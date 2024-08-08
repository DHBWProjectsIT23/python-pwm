import sqlite3

from src.config import db_path


def connect_to_db() -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database and initializes the
    necessary tables if they do not already exist.

    The connection is configured to parse declared types (e.g., custom types)
    and initializes the database schema by calling `initialize_tables`.

    Returns:
        sqlite3.Connection: The SQLite connection object, which can be used
                             to interact with the database.
    """
    connection = sqlite3.connect(db_path(), detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    initialize_tables(cursor)

    return connection


def initialize_tables(cursor: sqlite3.Cursor) -> None:
    """
    Initializes the necessary tables in the SQLite database if they do not
    already exist.

    This function creates the `passwords` and `users` tables, ensuring that
    the database schema is set up for storing password and user information.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object used for executing
                                 SQL commands.

    Returns:
        None: This function does not return any value. It modifies the database
              schema directly.
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
        salt BLOB NOT NULL,
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
