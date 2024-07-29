import asyncio
import os
import curses
import sqlite3
import sys
from curses import wrapper
from typing import TYPE_CHECKING, Callable

import controller.connection
from controller.user import insert_user
from model.password import (
    Password,
    adapt_password,
    convert_password,
)
from model.metadata import Metadata
from model.user import User
from tui.tui import tui_main
from crypto.hashing import hash_sha256
from controller.user import validate_login
from controller.password import insert_password_information

from model.password_information import (
    PasswordInformation,
    adapt_password_information,
    convert_password_information,
)

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


CursesMain = Callable[[Window], None]


def main() -> None:
    sqlite3.register_converter("password", convert_password)
    sqlite3.register_converter("password_information", convert_password_information)
    sqlite3.register_adapter(Password, adapt_password)
    sqlite3.register_adapter(PasswordInformation, adapt_password_information)
    if len(sys.argv) > 1:
        asyncio.run(cli_main())
    else:
        curses_main: CursesMain = tui_main
        wrapper(curses_main)


async def cli_main() -> None:
    print("Connecting to DB...")
    db_path: str = "test.db"
    connection_tuple: tuple[sqlite3.Connection, sqlite3.Cursor] = (
        controller.connection.connect_to_db(db_path)
    )
    connection: sqlite3.Connection = connection_tuple[0]
    cursor: sqlite3.Cursor = connection_tuple[1]

    username = "admin"
    password = "admin"
    print(f"Username: {username}")
    print(f"Password: {password}")

    print(f"{validate_login(cursor, username, password)}")

    # test_user_password = Password("test_pw", Metadata())
    # test_user: User = User(hash_sha256(b"test_user"), test_user_password)
    # #
    # admin_user_password = Password("admin", Metadata())
    # admin_user = User(hash_sha256(b"admin"), admin_user_password)
    #
    # test_password: Password = Password("tes_3", Metadata())
    # test_password_information = PasswordInformation(
    #     test_user, test_password, "cool_password", "Okay then"
    # )
    #
    # # insert_password_information(cursor, test_password_information)
    # # connection.commit()

    # connection.commit()

    # username: str = sys.argv[1]
    #
    # user: User = retrieve_user_by_name(cursor, username)
    # print(user.username.hex())
    #
    # for i in range(3):
    #     password = getpass.getpass(f"Password for {username}: ")
    #     if validate_login(cursor, username, password):
    #         print("Password correct")
    #         break
    #     print("Wrong password")
    #     if i == 2:
    #         print("To many failed password attempts")
    #         sys.exit(1)

    # password = Password("admin", Metadata())
    # user = User("admin", password)
    # password_information = PasswordInformation(
    #     user, "test_username", "test_email", "test_use_case"
    # )
    # decryptor = password.encrypt_password()
    # pickled_password = pickle.dumps(password)

    # print(user.password.password.hex())

    # print("")
    # print("")
    # print("")
    # task_api = asyncio.create_task(check_password(b"admin"))
    # print("I am written after the async call")
    # await task_api

    # cursor.execute("INSERT INTO passwords(data) VALUES(?)", (pickled_password,))
    # connection.commit()
    #
    # cursor.execute("SELECT data FROM passwords LIMIT 5")
    # for row in cursor:
    #     password = pickle.loads(row[0])
    #     print(password.password)
    #     decrypted_password = decrypt_password_aes256(decryptor, password.password)
    #     print(f"Decrypted Password after db: {decrypted_password}")

    connection.close()


def add_test_users(cursor: sqlite3.Cursor):
    admin_password = Password("admin", Metadata())
    admin_user = User(hash_sha256(b"admin"), admin_password)

    insert_user(cursor, admin_user)

    test_password = Password("test", Metadata())
    test_user = User(hash_sha256(b"test"), test_password)

    insert_user(cursor, test_user)


def add_test_passwords(cursor: sqlite3.Cursor, user: User):
    test_password_1 = Password("test_password_1", Metadata())
    test_password_information_1 = PasswordInformation(
        user, test_password_1, "Test password", "test@test.com"
    )
    test_password_2 = Password("test_password_2", Metadata())
    test_password_information_2 = PasswordInformation(
        user, test_password_2, "Test password", "test@test.com"
    )
    test_password_3 = Password("test_password_3", Metadata())
    test_password_information_3 = PasswordInformation(
        user, test_password_3, "Test password", "test@test.com"
    )
    test_password_4 = Password("test_password_4", Metadata())
    test_password_information_4 = PasswordInformation(
        user, test_password_4, "Test password", "test@test.com"
    )
    test_password_5 = Password("test_password_5", Metadata())
    test_password_information_5 = PasswordInformation(
        user, test_password_5, "Test password", "test@test.com"
    )

    insert_password_information(cursor, test_password_information_1)
    insert_password_information(cursor, test_password_information_2)
    insert_password_information(cursor, test_password_information_3)
    insert_password_information(cursor, test_password_information_4)
    insert_password_information(cursor, test_password_information_5)


if __name__ == "__main__":
    main()
