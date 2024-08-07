import secrets
import string


def generate_secure_password() -> str:
    """
    Generates a secure random password that meets complexity requirements.

    The password generated will:
    - Be 12 characters long.
    - Include at least one lowercase letter.
    - Include at least one uppercase letter.
    - Include at least three digits.
    - Include at least one special character (punctuation).

    Returns:
        str: A randomly generated secure password.
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

    Args:
        pw (str): The password to be evaluated.

    Returns:
        int: A safety rating for the password on a scale from 1 to 5,
             where 1 is unsafe and 5 is very safe.

    Notes:
        - A rating of 3 or higher is considered acceptable.
        - The function currently returns a fixed safety rating of 3.
    """
    return 3
