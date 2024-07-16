import datetime
import os


class Metadata:
    def __init__(self) -> None:
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        self.last_accessed_at = datetime.datetime.now()
        self.created_by = os.getlogin()
        self.modified_by = os.getlogin()
        self.last_accessed_by = os.getlogin()

    def access(self) -> None:
        self.last_accessed_at = datetime.datetime.now()
        self.last_accessed_by = os.getlogin()

    def modify(self) -> None:
        self.access()
        self.modified_at = datetime.datetime.now()
        self.modified_by = os.getlogin()

    def encrypt(self, key: bytes) -> "EncryptedMetadata":
        """
        PLACEHOLDER - Data should be encrypted
        """
        return EncryptedMetadata(self, key)


class EncryptedMetadata:
    def __init__(self, metadata: Metadata, key: bytes):
        """
        PLACEHOLDER - Data should be encrypted
        """
        self.created_at = metadata.created_at
        self.modified_at = metadata.modified_at
        self.last_accessed_at = metadata.last_accessed_at
        self.created_by = metadata.created_by
        self.modified_by = metadata.modified_by
        self.last_accessed_by = metadata.last_accessed_by

    def decrypt(self, key: bytes) -> Metadata:
        """
        PLACEHOLDER - Data should be decrypted
        """
        metadata = Metadata()
        metadata.created_at = self.created_at
        metadata.modified_at = self.modified_at
        metadata.last_accessed_at = self.last_accessed_at
        metadata.created_by = self.created_by
        metadata.modified_by = self.modified_by
        metadata.last_accessed_by = self.last_accessed_by
        return metadata
