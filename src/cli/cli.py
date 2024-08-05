import asyncio
import sqlite3

from src.controller.connection import connect_to_db, DB_PATH
from src.controller.password import (
    dummy_encrypt_fernet,
    insert_password_information,
    retrieve_password_information,
    update_password_information,
)
from src.controller.user import insert_user, validate_login
from src.crypto import password_util
from src.crypto.hashing import hash_sha256
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.user import User


async def run_cli(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    username = "admin"
    password = "admin"
    print(f"Username: {username}")
    print(f"Password: {password}")

    user = User.new("test", "test")
    user.set_clear_password("test")
    pw = retrieve_password_information(cursor, user)[-1]
    print(f"Note full: {pw.note.decode()}")

    note = pw.note.decode()
    inset = len("Note: ")
    max_length = 10
    line_amount = len(note) // max_length
    lines: list[str] = []
    position = 0
    for i in range(line_amount):
        if position + max_length >= len(note):
            break
        print(f"Position: {position} / {len(note)}")
        lines.append(note[position : position + max_length])
        position += max_length

    for i, line in enumerate(lines):
        print(f"Line: {line} - {len(line)}")
        # addstr(y + 2 + i, inset, line)

    # print(f"{validate_login(cursor, username, password)}")
    # retrieve_password_information(cursor, hash_sha256(b"test"))


def main() -> None:
    print("Running in cli mode")
    with connect_to_db(DB_PATH) as connection:
        asyncio.run(run_cli(connection, connection.cursor()))
