# type : ignore
import sqlite3
import os
import sys


path = os.path.dirname(os.path.abspath(__file__))
sourcePath = os.path.join(path, "src")
sys.path.insert(0, sourcePath)

from src.controller.connection import connect_to_db
from src.controller.connection import DB_PATH
from src.model.user import User
from src.crypto.hashing import hash_sha256
from src.controller.user import insert_user
from src.controller.password import insert_password_information
from src.model.password import Password, convert_password, adapt_password
from src.model.password_information import (
    PasswordInformation,
    convert_password_information,
    adapt_password_information,
)


def main() -> None:
    sqlite3.register_converter("password", convert_password)
    sqlite3.register_converter("password_information", convert_password_information)
    sqlite3.register_adapter(Password, adapt_password)
    sqlite3.register_adapter(PasswordInformation, adapt_password_information)
    with connect_to_db(DB_PATH) as connection:
        cursor = connection.cursor()
        add_test_users(cursor)
        i = 0
        while i < 10:
            add_test_passwords(cursor, User.new("test", "test"))
            i += 1
        connection.commit()


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
    test_password_information_1.encrypt(b"FakeKey")
    test_password_2 = Password("test_password_2")
    test_password_information_2 = PasswordInformation(
        user, test_password_2, "Linux PC", "simonTest"
    )
    test_password_information_2.encrypt(b"FakeKey")
    test_password_3 = Password("test_password_3")
    test_password_information_3 = PasswordInformation(
        user, test_password_3, "Test Password", "test@test.com"
    )
    test_password_information_3.encrypt(b"FakeKey")
    test_password_4 = Password("test_password_4")
    test_password_information_4 = PasswordInformation(
        user, test_password_4, "www.youtube.com", "tmp@test.de"
    )
    test_password_information_4.encrypt(b"FakeKey")
    test_password_5 = Password("test_password_5")
    test_password_information_5 = PasswordInformation(
        user, test_password_5, "www.gmail.com", "test@gmail.com"
    )
    test_password_information_5.encrypt(b"FakeKey")

    insert_password_information(cursor, test_password_information_1)
    insert_password_information(cursor, test_password_information_2)
    insert_password_information(cursor, test_password_information_3)
    insert_password_information(cursor, test_password_information_4)
    insert_password_information(cursor, test_password_information_5)


if __name__ == "__main__":
    main()
