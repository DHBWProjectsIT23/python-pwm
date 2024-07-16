import asyncio
import getpass
import hashlib
import pickle
import sqlite3
import sys
from curses import wrapper

import requests
from api.placeholder import check_password
from crypto.placeholder import decrypt_password_aes256
from crypto.placeholder_2 import hash_sha256
from db.connection import connect_to_db
from model.metadata import Metadata
from model.password import Password
from tui.tui import tui_main

from src.model.password_information import PasswordInformation
from src.model.user import User


def main() -> None:
    if len(sys.argv) > 1:
        asyncio.run(cli_main())
    else:
        wrapper(tui_main)


async def cli_main() -> None:
    print("Connecting to DB")
    connection, cursor = connect_to_db("test.db")
    print("Connected to DB")

    username = sys.argv[1]
    print(f"Given username: {username}")

    result = cursor.execute(
        "SELECT * FROM users WHERE username=?", (hash_sha256(username.encode()),)
    )

    user = result.fetchone()
    if user is None:
        print("User not found")
        sys.exit(1)

    for i in range(3):
        password = getpass.getpass(f"Password for {username}: ")
        if hash_sha256(password.encode()) == user[1]:
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
    # # decryptor = password.encrypt_password()
    # # pickled_password = pickle.dumps(password)
    #
    # print(user.password.password.hex())
    #
    # print("")
    # print("")
    # print("")
    # task_api = asyncio.create_task(check_password(password.password))
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
