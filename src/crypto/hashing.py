import hashlib


def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()
