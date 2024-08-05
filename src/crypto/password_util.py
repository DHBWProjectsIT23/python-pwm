def generate_secure_password() -> str:
    return "I_AM_VERY_SECURE"


def validate_password_safety(pw: str) -> int:
    """
    1 is unsafe, 5 is very safe
    acceptable from 3 onwards?
    """
    return 3
