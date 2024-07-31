import pickle
from typing import Optional

from src.crypto.hashing import hash_sha256
from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet

from .metadata import EncryptedMetadata, Metadata


class Password:
    def __init__(self, password: str, metadata: Metadata = Metadata()):
        self.is_encrypted: bool = False
        self.password: bytes = str.encode(password)
        self.metadata: Optional[Metadata] = metadata
        self.encrypted_metadata: Optional[EncryptedMetadata] = None
        self.is_master = False

    def encrypt(self, key: bytes) -> None:
        self.is_encrypted = True
        self._encrypt_password()
        self._encrypt_metadata(key)

    def decrypt(self, key: bytes) -> None:
        self.is_encrypted = False
        self._decrypt_password()
        self._decrypt_metadata(key)

    def _encrypt_password(self) -> None:
        self.password = dummy_encrypt_fernet(self.password)
        # raise NotImplementedError

    def _decrypt_password(self) -> None:
        self.password = dummy_decrypt_fernet(self.password)
        # raise NotImplementedError

    def _encrypt_metadata(self, key: bytes) -> None:
        if self.encrypted_metadata is not None:
            raise ValueError("Metadata already encrypted")
        if self.metadata is None:
            raise ValueError("Metadata not set")

        self.metadata.access()
        self.encrypted_metadata = self.metadata.encrypt(key)
        self.metadata = None

    def _decrypt_metadata(self, key: bytes) -> None:
        if self.encrypted_metadata is None:
            raise ValueError("Metadata not encrypted")
        if self.metadata is not None:
            raise ValueError("Metadata already decrypted")

        self.metadata = self.encrypted_metadata.decrypt(key)
        self.encrypted_metadata = None

    def make_master(self) -> None:
        if self.is_master:
            raise ValueError("Password is already master")
        if self.is_encrypted:
            raise ValueError("Password is encrypted")
        if self.metadata is None:
            raise ValueError("Metadata not set")

        self.metadata.modify()
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


class PasswordList(list[Password]):
    pass
