import asyncio
import sqlite3
import sys
from curses import wrapper
from typing import TYPE_CHECKING, Callable

import controller.connection
from model.password import (
    Password,
    adapt_password,
    convert_password,
)
from tui.tui import tui_main

from src.model.password_information import (
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


if __name__ == "__main__":
    main()
