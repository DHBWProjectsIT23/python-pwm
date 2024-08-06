from __future__ import annotations

import datetime
import pickle

from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet


class Metadata:
    def __init__(self) -> None:
        self.created_at: datetime.datetime = datetime.datetime.now()
        self.last_modified: datetime.datetime = datetime.datetime.now()

    def modify(self) -> None:
        self.last_modified = datetime.datetime.now()

    def encrypt(self, key: bytes) -> EncryptedMetadata:
        return EncryptedMetadata(self, key)


class EncryptedMetadata:
    def __init__(self, metadata: Metadata, key: bytes) -> None:
        self.created_at: bytes = dummy_encrypt_fernet(pickle.dumps(metadata.created_at))
        self.modified_at: bytes = dummy_encrypt_fernet(
            pickle.dumps(metadata.last_modified)
        )

    def access(self) -> None:
        """
        TBC: Here because Union sth mypy whatever
        """
        raise TypeError("Can't access encrypted Metadata")

    def modify(self) -> None:
        """
        TBC: Here because Union sth mypy whatever
        """
        raise TypeError("Can't modify encrypted Metadata")

    def decrypt(self, key: bytes) -> Metadata:
        metadata = Metadata()
        metadata.created_at: datetime.datetime = pickle.loads(
            dummy_decrypt_fernet(self.created_at)
        )
        metadata.last_modified: datetime.datetime = pickle.loads(
            dummy_decrypt_fernet(self.modified_at)
        )
        return metadata
