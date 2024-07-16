import hashlib
import base64
from cryptography.fernet import Fernet


def encrypt_fernet(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_fernet(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(data)


def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()
