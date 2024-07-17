import asyncio
import sqlite3
import sys
import getpass

from curses import wrapper

from crypto.hashing import hash_sha256
from model.metadata import Metadata
from db.connection import connect_to_db
from db.retrieve import retrieve_user_by_name
from model.password import Password, adapt_password, convert_password
from model.user import User
from tui.tui import tui_main
from api.placeholder import check_password

import curses
import time
from curses.textpad import Textbox, rectangle
from typing import TYPE_CHECKING, Callable
from src.db.placeholder import validate_login
from src.db.insert import insert_user


if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


CursesMain = Callable[[Window], None]


def main() -> None:
    sqlite3.register_converter("password", convert_password)
    sqlite3.register_adapter(Password, adapt_password)
    if len(sys.argv) > 1:
        asyncio.run(cli_main())
    else:
        curses_main: CursesMain = tui_main
        wrapper(curses_main)


async def cli_main() -> None:
    print("Connecting to DB...")
    db_path: str = "test.db"
    connection_tuple: tuple[sqlite3.Connection, sqlite3.Cursor] = connect_to_db(db_path)
    connection: sqlite3.Connection = connection_tuple[0]
    cursor: sqlite3.Cursor = connection_tuple[1]
    print("")

    username: str = sys.argv[1]

    user: User = retrieve_user_by_name(cursor, username)
    print(user.username.hex())

    for i in range(3):
        password = getpass.getpass(f"Password for {username}: ")
        if validate_login(cursor, username, password):
            print("Password correct")
            break
        print("Wrong password")
        if i == 2:
            print("To many failed password attempts")
            sys.exit(1)

    # password = Password("admin", Metadata())
    # user = User("admin", password)
    # password_information = PasswordInformation(
    #     user, "test_username", "test_email", "test_use_case"
    # )
    # decryptor = password.encrypt_password()
    # pickled_password = pickle.dumps(password)

    print(user.password.password.hex())

    print("")
    print("")
    print("")
    task_api = asyncio.create_task(check_password(b"admin"))
    print("I am written after the async call")
    await task_api

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
