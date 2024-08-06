from __future__ import annotations

import datetime
import pickle

from src.crypto.placeholder import dummy_decrypt_fernet, dummy_encrypt_fernet


class Metadata:
    """
    A class representing metadata for an object.

    Attributes:
        created_at (datetime.datetime): The timestamp when the metadata was created.
        last_modified (datetime.datetime): The timestamp when the metadata was last modified.
    """
    def __init__(self) -> None:
        """
        Initializes Metadata with current timestamp for creation and modification.
        """
        self.created_at: datetime.datetime = datetime.datetime.now()
        self.last_modified: datetime.datetime = datetime.datetime.now()

    def modify(self) -> None:
        """
        Updates the last_modified timestamp to the current time.
        """
        self.last_modified = datetime.datetime.now()

    def encrypt(self, key: bytes) -> EncryptedMetadata:
        """
        Encrypts the Metadata instance using the provided key.

        Args:
            key (bytes): The encryption key.

        Returns:
            EncryptedMetadata: An instance of EncryptedMetadata containing the encrypted metadata.
        """
        return EncryptedMetadata(self, key)


class EncryptedMetadata:
    """
    A class representing encrypted metadata.

    Attributes:
        created_at (bytes): The encrypted timestamp of when the metadata was created.
        modified_at (bytes): The encrypted timestamp of when the metadata was last modified.
    """
    def __init__(self, metadata: Metadata, key: bytes) -> None:
        """
        Initializes EncryptedMetadata by encrypting the provided Metadata using the provided key.

        Args:
            metadata (Metadata): The Metadata instance to be encrypted.
            key (bytes): The encryption key.
        """
        self.created_at: bytes = dummy_encrypt_fernet(pickle.dumps(metadata.created_at))
        self.modified_at: bytes = dummy_encrypt_fernet(
            pickle.dumps(metadata.last_modified)
        )

    def access(self) -> None:
        """
        Prevents access to the encrypted metadata.

        Raises:
            TypeError: Always raises an exception since encrypted metadata should not be accessed directly.
        """
        raise TypeError("Can't access encrypted Metadata")

    def modify(self) -> None:
        """
        Prevents modification of the encrypted metadata.

        Raises:
            TypeError: Always raises an exception since encrypted metadata should not be modified directly.
        """
        raise TypeError("Can't modify encrypted Metadata")

    def decrypt(self, key: bytes) -> Metadata:
        """
        Decrypts the encrypted metadata using the provided key.

        Args:
            key (bytes): The decryption key.

        Returns:
            Metadata: An instance of Metadata with the decrypted data.
        """
        metadata = Metadata()
        metadata.created_at: datetime.datetime = pickle.loads(
            dummy_decrypt_fernet(self.created_at)
        )
        metadata.last_modified: datetime.datetime = pickle.loads(
            dummy_decrypt_fernet(self.modified_at)
        )
        return metadata
