from cryptography.fernet import Fernet


def encrypt_fernet(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_fernet(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(data)