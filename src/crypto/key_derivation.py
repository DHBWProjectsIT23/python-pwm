import os

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def scrypt_derive(pw: bytes, salt: bytes) -> bytes:
    """
    Derives password with Scrypt in preperation for AES-Encryption.

    Args:
        pw (bytes): The password to be derived.
        salt (bytes): The salt used for derivation.
    """
    kdf = Scrypt(salt, 32, 2**14, 8, 1)
    return kdf.derive(pw)


def scrypt_verify(pw: bytes, derived_key: bytes, salt: bytes) -> bool:
    """
    Checks if a given password was used to generate the given key.

    Args:
        pw (bytes): the password that should be checked
        derived_key (bytes): The derived key.
        salt (bytes): The salt used for derivation.
    """
    kdf = Scrypt(salt, 32, 2**14, 8, 1)
    try:
        kdf.verify(pw, derived_key)
        return True
    except:
        return False
