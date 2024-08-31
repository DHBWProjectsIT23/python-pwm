"""
Provides functions for generating secure passwords and evaluating password safety.
"""

import secrets
import string


def generate_secure_password() -> str:
    """
    Generates a secure random password that meets complexity requirements.

    The password generated will:
    - Be exactly 12 characters long.
    - Include at least one lowercase letter.
    - Include at least one uppercase letter.
    - Include at least three digits.
    - Include at least one special character (punctuation).

    Returns:
        str: A randomly generated secure password that adheres to the complexity requirements.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(12))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
            and any(c in string.punctuation for c in password)
        ):
            break

    return password


def validate_password_safety(pw: str) -> int:
    """
    Evaluates the safety of a given password based on its complexity.

    The password safety is rated on a scale from 1 to 5:
    - 1: Very weak
    - 2: Weak
    - 3: Average
    - 4: Strong
    - 5: Very strong

    Args:
        pw (str): The password to be evaluated.

    Returns:
        int: A safety rating for the password based on its length and character composition.
    """
    safetypoints = 0
    special_chars = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

    if len(pw) < 6:
        return 0

    if len(pw) > 16:
        safetypoints += 1

    if any(char.islower() for char in pw):
        safetypoints += 1

    if any(char.isupper() for char in pw):
        safetypoints += 1

    if any(char.isdigit() for char in pw):
        safetypoints += 1

    if any(char in special_chars for char in pw):
        safetypoints += 1

    return safetypoints
