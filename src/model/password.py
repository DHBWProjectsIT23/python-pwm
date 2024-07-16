import pickle
from typing import Optional

from cryptography.hazmat.primitives.ciphers import CipherContext

from src.crypto.placeholder import encrypt_password_aes256
from src.crypto.placeholder_2 import (
    hash_sha256,
    encrypt_fernet,
    decrypt_fernet,
)

from .metadata import Metadata


class Password:
    def __init__(self, password: str, metadata: Metadata):
        self.is_encrypted: bool = False
        self.password: bytes = str.encode(password)
        self.metadata: Optional[Metadata] = metadata
        self.is_master = False

    def encrypt_password(self) -> CipherContext:
        self.is_encrypted = True
        self.password, decryptor = encrypt_password_aes256(self.password)
        return decryptor

    def encrypt_metadata(self, key: bytes) -> bytes:
        raise NotImplementedError
        # self.metadata.accessed()
        # pickled_metadata = pickle.dumps(self.metadata)
        # return encrypt_fernet(pickled_metadata, key)

    def decrypt_metadata(self, key: bytes, encrypted_metadata: bytes) -> None:
        raise NotImplementedError
        # decrypted_metadata = decrypt_fernet(encrypted_metadata, key)
        # if not isinstance(decrypted_metadata, bytes):
        #     raise TypeError("Bytes object expected")
        # self.metadata = pickle.loads(decrypted_metadata)

    def make_master(self) -> None:
        self.password = hash_sha256(self.password)
        self.is_master = True
