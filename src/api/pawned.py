"""
This module checks if a password has been exposed in data breaches using the Pwned Passwords API.

Main Function:
    check_password(password: bytes) -> int: 
        Hashes the password with SHA-1 and queries the API to find the number of breaches.

Dependencies:
    requests: For making HTTP requests.
    src.crypto.hashing: For hashing the password.

Usage:
    occurrences = await check_password(b'my_secure_password')
"""
import requests

from src.crypto.hashing import hash_sha1


async def check_password(password: bytes) -> int:
    """
    Checks if the given password has been exposed in data breaches using the Pwned Passwords API.

    This function queries the Pwned Passwords API to determine if the given password 
    (hashed with SHA-1) has been found in data breaches and returns the number of occurrences.

    Args:
        password (bytes): The password to check, provided as a bytes object. 
        The password will be hashed using SHA-1.

    Returns:
        int: The number of times the password has been found in data breaches. 
        Returns 0 if the password is not found.

    Raises:
        requests.RequestException: If the request to the Pwned Passwords API fails.
    """

    password_hash = hash_sha1(password).hex()
    first_five = password_hash[:5]

    request = requests.get(
        f"https://api.pwnedpasswords.com/range/{first_five}", timeout=5
    )
    occurrences = 0
    for row in request.text.splitlines():
        full_hash_with_occurrences = first_five + row
        full_hash, response_occurrences = full_hash_with_occurrences.split(":")
        if full_hash.lower() == password_hash:
            occurrences += int(response_occurrences)

    return occurrences
