"""
Provides functions for encryption and decryption using the Fernet symmetric encryption scheme.
"""

import base64

from cryptography.fernet import Fernet


def encrypt_fernet(data: bytes, key: bytes) -> bytes:
    """
    Encrypts the given data using the Fernet encryption scheme with the provided key.

    Args:
        data (bytes): The data to be encrypted, in bytes format.
        key (bytes): The 32-byte key for Fernet encryption. This key will be
                     encoded to base64 format.

    Returns:
        bytes: The encrypted data.
    """
    base64_key = base64.urlsafe_b64encode(key)
    f = Fernet(base64_key)
    return f.encrypt(data)


def decrypt_fernet(data: bytes, key: bytes) -> bytes:
    """
    Decrypts the given Fernet-encrypted data using the provided key.

    Args:
        data (bytes): The encrypted data in bytes format.
        key (bytes): The 32-byte key for Fernet decryption. This key will be
                     encoded to base64 format.

    Returns:
        bytes: The decrypted data.
    """
    base64_key = base64.urlsafe_b64encode(key)
    f = Fernet(base64_key)
    return f.decrypt(data)
