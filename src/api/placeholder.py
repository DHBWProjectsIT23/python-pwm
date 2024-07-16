import hashlib
import requests


async def check_password(password: bytes) -> None:
    password_hash = hashlib.sha1(password)
    first_five = password_hash.hexdigest()[:5]

    x = requests.get(f"https://api.pwnedpasswords.com/range/{first_five}")
    print("Api response:")
    is_pwned = False
    for row in x.text.splitlines():
        full_hash_with_occurences = first_five + row
        full_hash, occurences = full_hash_with_occurences.split(":")
        if full_hash.lower() == password_hash.hexdigest():
            is_pwned = True
            print(f"Oh no! Your password has been seen {int(occurences):_} times")

    if not is_pwned:
        print("Your password has not been seen before!")
