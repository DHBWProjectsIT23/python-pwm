import asyncio
import sqlite3

from src.controller.connection import connect_to_db
from src.controller.password import (
    insert_password_information,
    retrieve_password_information,
    update_password_information,
)

from src.controller.user import insert_user, validate_login
from src.crypto import password_util
from src.crypto.hashing import hash_sha256
from src.import_export.import_data import import_json, verify_required_key
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.user import User
from src.import_export.export_data import _convert_to_dict, export_to_json


async def run_cli(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Executes the CLI operations for managing users and passwords.

    Args:
        connection (sqlite3.Connection): The SQLite connection object.
        cursor (sqlite3.Cursor): The SQLite cursor object.

    Returns:
        None
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
    user = User.new("test", "test")


def main() -> None:
    """
    The main entry point for running the CLI application.

    Establishes a connection to the database and runs the CLI operations.

    Returns:
        None
    """
    print("Running in cli mode")
    with connect_to_db() as connection:
        asyncio.run(run_cli(connection, connection.cursor()))
