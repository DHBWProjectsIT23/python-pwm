"""
Provides functions for key derivation and verification using the Scrypt algorithm.
"""
import os
from typing import Optional

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey


def scrypt_derive(pw: bytes, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
    """
    Derives a key from the given password using the Scrypt key derivation function.

    Args:
        pw (bytes): The password to be derived.
        salt (Optional[bytes]): The salt to use for key derivation. 
        If not provided, a new salt will be generated.

    Returns:
        tuple[bytes, bytes]: A tuple containing the derived key and the salt used.
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = Scrypt(salt, 32, 2**14, 8, 1)
    return kdf.derive(pw), salt


def scrypt_verify(pw: bytes, derived_key: bytes, salt: bytes) -> bool:
    """
    Verifies if the given password matches the derived key using the Scrypt key derivation function.

    Args:
        pw (bytes): The password to check.
        derived_key (bytes): The derived key to compare against.
        salt (bytes): The salt used during key derivation.

    Returns:
        bool: True if the password matches the derived key, False otherwise.
    """
    kdf = Scrypt(salt, 32, 2**14, 8, 1)
    try:
        kdf.verify(pw, derived_key)
        return True
    except InvalidKey:
        return False
