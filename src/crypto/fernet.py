from cryptography.fernet import Fernet
import base64


def encrypt_fernet(data: bytes, key: bytes) -> bytes:
    base64_key = base64.urlsafe_b64encode(key)
    f = Fernet(base64_key)
    return f.encrypt(data)


def decrypt_fernet(data: bytes, key: bytes) -> bytes:
    base64_key = base64.urlsafe_b64encode(key)
    f = Fernet(base64_key)
    return f.decrypt(data)