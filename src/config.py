import os

from src.crypto.hashing import hash_sha256


def db_path() -> str:
    return os.getenv("DB_PATH") or hash_sha256("ppwm".encode()).hex()[:12]
