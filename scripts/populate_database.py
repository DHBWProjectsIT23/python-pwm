# pylint: disable=C
# type: ignore
import os
import sqlite3
import sys

path = os.path.dirname(os.path.abspath(__file__))
sourcePath = os.path.join(path, "..")
sourcePath = os.path.abspath(sourcePath)
sys.path.append(sourcePath)

from src.controller.connection import connect_to_db
from src.controller.password import insert_password_information
from src.controller.user import insert_user
from src.crypto.hashing import hash_sha256
from src.model.password import Password, adapt_password, convert_password
from src.model.password_information import PasswordInformation
from src.model.user import User
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    sqlite3.register_converter("password", convert_password)
    sqlite3.register_adapter(Password, adapt_password)
    with connect_to_db() as connection:
        cursor = connection.cursor()
        add_test_users(cursor)
        for i in range(7):
            add_test_passwords(cursor, User.new("Test", "TestUser2103"), i)
        connection.commit()


def add_test_users(cursor: sqlite3.Cursor) -> None:
    admin_password = Password("AdminUser2103")
    admin_user = User(hash_sha256(b"Admin"), admin_password)

    insert_user(cursor, admin_user)

    test_password = Password("TestUser2103")
    test_user = User(hash_sha256(b"Test"), test_password)

    insert_user(cursor, test_user)


def add_test_passwords(cursor: sqlite3.Cursor, user: User, index: int) -> None:
    user.set_clear_password("TestUser2103")
    test_password_1 = Password(f"test_password_1_{index}")
    test_password_information_1 = PasswordInformation(
        user, test_password_1, f"www.github{index}.com", "simon@test.com"
    )
    test_password_2 = Password(f"test_password_2_{index}")
    test_password_information_2 = PasswordInformation(
        user, test_password_2, f"Linux PC {index}", "simonTest"
    )
    test_password_3 = Password(f"test_password_3_{index}")
    test_password_information_3 = PasswordInformation(
        user, test_password_3, f"Test Password {index}", "test@test.com"
    )
    test_password_4 = Password(f"test_password_4_{index}")
    test_password_information_4 = PasswordInformation(
        user, test_password_4, f"www.youtube{index}.com", "tmp@test.de"
    )
    test_password_5 = Password(f"test_password_5_{index}")
    test_password_information_5 = PasswordInformation(
        user, test_password_5, f"www.gmail{index}.com", "test@gmail.com"
    )

    insert_password_information(cursor, test_password_information_1)
    insert_password_information(cursor, test_password_information_2)
    insert_password_information(cursor, test_password_information_3)
    insert_password_information(cursor, test_password_information_4)
    insert_password_information(cursor, test_password_information_5)


if __name__ == "__main__":
    main()
