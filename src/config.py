import os

from src.crypto.hashing import hash_sha256

MIN_SIZE: tuple[int, int] = (35, 80)


def db_path() -> str:
    """
    Retrieves the database path from the environment variable or generates a
    default path based on a hashed string.

    This function checks for the presence of an environment variable named 
    'DB_PATH'. If the environment variable is not set, it generates a default
    path using a hashed string 'ppwm' with the SHA-256 algorithm and truncates 
    it to the first 12 characters.

    Returns:
        str: The database path either from the environment variable or the 
             default generated path.
    """
    return os.getenv("DB_PATH") or hash_sha256("ppwm".encode()).hex()[:12]
