import hashlib


def hash_sha256(data: bytes) -> bytes:
    if len(data) == 0:
        raise ValueError("Data to hash is empty")
    return hashlib.sha256(data).digest()


def hash_sha1(data: bytes) -> bytes:
    if len(data) == 0:
        raise ValueError("Data to hash is empty")
    return hashlib.sha1(data).digest()
