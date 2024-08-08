import asyncio
import sqlite3

from src.controller.connection import connect_to_db
from src.controller.password import (
    retrieve_password_information,
)
from src.model.password_information import PasswordInformation
from src.model.user import User


async def run_cli(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Executes the CLI operations for managing and retrieving user and password data.

    This asynchronous function performs various operations, such as retrieving password information
    for a specific user and filtering the results based on a criterion. It demonstrates how to interact
    with the SQLite database using the provided connection and cursor.

    Args:
        connection (sqlite3.Connection): The SQLite connection object used to interact with the database.
        cursor (sqlite3.Cursor): The SQLite cursor object used for executing SQL queries.

    Returns:
        None: This function does not return any value. It prints the results of the operations to the console.
    """
    # username = "admin"
    # password = "admin"
    # print(f"Username: {username}")
    # print(f"Password: {password}")
    #
    # user = User.new("test", "test")
    # user.set_clear_password("test")
    # pw = retrieve_password_information(cursor, user)
    # pws = import_json("import.json", user)
    # for p in pws:
    #     print(p)
    # send_auth_mail("simon21.blum@gmail.com", "513")
    _ = connection
    user = User.new("test", "test")
    user.set_clear_password("test")
    pws = retrieve_password_information(cursor, user)
    print(len(pws))
    pws = list(
        filter(PasswordInformation.create_password_filter("www.github.com"), pws)
    )
    print(len(pws))


def main() -> None:
    """
    The main entry point for running the CLI application.

    This function sets up the database connection and invokes the CLI operations defined in `run_cli`.
    It demonstrates how to initialize the application and manage the database connection lifecycle.

    Returns:
        None
    """
    print("Running in cli mode")
    with connect_to_db() as connection:
        asyncio.run(run_cli(connection, connection.cursor()))
