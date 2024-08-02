import requests
from src.crypto.hashing import hash_sha1


async def check_password(password: bytes) -> int:
    password_hash = hash_sha1(password).hex()
    first_five = password_hash[:5]

    request = requests.get(
        f"https://api.pwnedpasswords.com/range/{first_five}", timeout=5
    )
    occurences = 0
    for row in request.text.splitlines():
        full_hash_with_occurences = first_five + row
        full_hash, response_occurences = full_hash_with_occurences.split(":")
        if full_hash.lower() == password_hash:
            occurences += int(response_occurences)

    return occurences
