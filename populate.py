# type : ignore
import os
import sqlite3
import sys

path = os.path.dirname(os.path.abspath(__file__))
sourcePath = os.path.join(path, "src")
sys.path.insert(0, sourcePath)

from src.controller.connection import DB_PATH, connect_to_db
from src.controller.password import insert_password_information
from src.controller.user import insert_user
from src.crypto.hashing import hash_sha256
from src.model.password import Password, adapt_password, convert_password
from src.model.password_information import PasswordInformation
from src.model.user import User


def main() -> None:
    sqlite3.register_converter("password", convert_password)
    sqlite3.register_adapter(Password, adapt_password)
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
    user.set_clear_password("test")
    test_password_1 = Password("test_password_1")
    test_password_information_1 = PasswordInformation(
        user, test_password_1, "www.github.com", "simon@test.com"
    )
    test_password_2 = Password("test_password_2")
    test_password_information_2 = PasswordInformation(
        user, test_password_2, "Linux PC", "simonTest"
    )
    test_password_3 = Password("test_password_3")
    test_password_information_3 = PasswordInformation(
        user, test_password_3, "Test Password", "test@test.com"
    )
    test_password_4 = Password("test_password_4")
    test_password_information_4 = PasswordInformation(
        user, test_password_4, "www.youtube.com", "tmp@test.de"
    )
    test_password_5 = Password("test_password_5")
    test_password_information_5 = PasswordInformation(
        user, test_password_5, "www.gmail.com", "test@gmail.com"
    )

    insert_password_information(cursor, test_password_information_1)
    insert_password_information(cursor, test_password_information_2)
    insert_password_information(cursor, test_password_information_3)
    insert_password_information(cursor, test_password_information_4)
    insert_password_information(cursor, test_password_information_5)


if __name__ == "__main__":
    main()
