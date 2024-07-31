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

    # add_test_users(cursor)
    # add_test_passwords(cursor, User.new("test", "test"))
    # connection.commit()

    print(f"{validate_login(cursor, username, password)}")
    retrieve_password_information(cursor, hash_sha256(b"test"))


def main() -> None:
    print("Running in cli mode")
    with connect_to_db(DB_PATH) as connection:
        asyncio.run(run_cli(connection, connection.cursor()))


def add_test_users(cursor: sqlite3.Cursor) -> None:
    admin_password = Password("admin")
    admin_user = User(hash_sha256(b"admin"), admin_password)

    insert_user(cursor, admin_user)

    test_password = Password("test")
    test_user = User(hash_sha256(b"test"), test_password)

    insert_user(cursor, test_user)


def add_test_passwords(cursor: sqlite3.Cursor, user: User) -> None:
    test_password_1 = Password("test_password_1")
    test_password_information_1 = PasswordInformation(
        user, test_password_1, "www.github.com", "simon@test.com"
    )
    test_password_1.encrypt("FakeKey")
    test_password_2 = Password("test_password_2")
    test_password_information_2 = PasswordInformation(
        user, test_password_2, "Linux PC", "simonTest"
    )
    test_password_2.encrypt("FakeKey")
    test_password_3 = Password("test_password_3")
    test_password_information_3 = PasswordInformation(
        user, test_password_3, "Test Password", "test@test.com"
    )
    test_password_3.encrypt("FakeKey")
    test_password_4 = Password("test_password_4")
    test_password_information_4 = PasswordInformation(
        user, test_password_4, "www.youtube.com", "tmp@test.de"
    )
    test_password_4.encrypt("FakeKey")
    test_password_5 = Password("test_password_5")
    test_password_information_5 = PasswordInformation(
        user, test_password_5, "www.gmail.com", "test@gmail.com"
    )
    test_password_5.encrypt("FakeKey")

    insert_password_information(cursor, test_password_information_1)
    insert_password_information(cursor, test_password_information_2)
    insert_password_information(cursor, test_password_information_3)
    insert_password_information(cursor, test_password_information_4)
    insert_password_information(cursor, test_password_information_5)
