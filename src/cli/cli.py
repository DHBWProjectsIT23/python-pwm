import asyncio
import sqlite3

from src.controller.connection import connect_to_db, DB_PATH
from src.controller.password import (
    insert_password_information,
    retrieve_password_information,
)
from src.controller.user import insert_user, validate_login
from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.user import User


async def run_cli(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    username = "admin"
    password = "admin"
    print(f"Username: {username}")
    print(f"Password: {password}")

    print(f"{validate_login(cursor, username, password)}")
    retrieve_password_information(cursor, hash_sha256(b"test"))


def main() -> None:
    print("Running in cli mode")
    with connect_to_db(DB_PATH) as connection:
        asyncio.run(run_cli(connection, connection.cursor()))
