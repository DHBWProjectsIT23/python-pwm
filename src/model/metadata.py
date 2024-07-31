from __future__ import annotations

import datetime


class Metadata:
    def __init__(self) -> None:
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        self.last_accessed_at = datetime.datetime.now()

    def access(self) -> None:
        self.last_accessed_at = datetime.datetime.now()

    def modify(self) -> None:
        self.access()
        self.modified_at = datetime.datetime.now()

    def encrypt(self, key: bytes) -> EncryptedMetadata:
        return EncryptedMetadata(self, key)


class EncryptedMetadata:
    def __init__(self, metadata: Metadata, key: bytes) -> None:
        self.created_at = metadata.created_at
        self.modified_at = metadata.modified_at
        self.last_accessed_at = metadata.last_accessed_at

    def access(self) -> None:
        raise TypeError("Can't access encrypted Metadata")

    def modify(self) -> None:
        raise TypeError("Can't modify encrypted Metadata")

    def decrypt(self, key: bytes) -> Metadata:
        metadata = Metadata()
        metadata.created_at = self.created_at
        metadata.modified_at = self.modified_at
        metadata.last_accessed_at = self.last_accessed_at
        return metadata
