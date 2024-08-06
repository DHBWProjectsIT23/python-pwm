import pickle
from typing import Optional

from src.crypto.hashing import hash_sha256
from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet
from src.exceptions.encryption_exception import EncryptionException


class Password:
    def __init__(self, password: str):
        self.is_encrypted: bool = False
        self.password: bytes = password.encode()
        self.is_master = False

    def encrypt(self, key: bytes) -> None:
        if self.is_master:
            raise EncryptionException("Master password can't be encrypted")
        if self.is_encrypted:
            return
        self.is_encrypted = True
        self._encrypt_password()

    def decrypt(self, key: bytes) -> None:
        if self.is_master:
            raise EncryptionException("Master password can't be decrypted")
        if not self.is_encrypted:
            return
        self.is_encrypted = False
        self._decrypt_password()

    def _encrypt_password(self) -> None:
        self.password = dummy_encrypt_fernet(self.password)
        # raise NotImplementedError

    def _decrypt_password(self) -> None:
        self.password = dummy_decrypt_fernet(self.password)
        # raise NotImplementedError

    def make_master(self) -> None:
        if self.is_master:
            raise ValueError("Password is already master")
        if self.is_encrypted:
            raise ValueError("Password is encrypted")

        self.password = hash_sha256(self.password)
        self.is_master = True

    def __call__(self) -> bytes:
        return self.password


def adapt_password(password: Password) -> bytes:
    if not password.is_encrypted and not password.is_master:
        raise TypeError("Password is not encrypted")

    return pickle.dumps(password)


def convert_password(password: bytes) -> Password:
    retrieved_password: Password = pickle.loads(password)
    if not isinstance(retrieved_password, Password):
        raise TypeError("Password expected")
    return retrieved_password
