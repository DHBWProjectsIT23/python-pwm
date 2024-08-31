"""
Provides AES encryption and decryption functionality.
"""

import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


def encrypt_aes(data: bytes, key: bytes) -> bytes:
    """
    Encrypts the given data using AES encryption with the provided key.

    Args:
        data (bytes): The data to be encrypted. Must be in bytes format.
        key (bytes): The 16, 24, or 32-byte encryption key for AES.

    Returns:
        bytes: The encrypted data, including the initialization vector (IV)
               prepended to the ciphertext.
    """
    iv = os.urandom(16)
    padder: padding.PaddingContext = padding.PKCS7(128).padder()
    padded_message: bytes = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return iv + ciphertext


def decrypt_aes(ciphertext: bytes, key: bytes) -> bytes:
    """
    Decrypts the given AES-encrypted data using the provided key.

    Args:
        ciphertext (bytes): The encrypted data, including the initialization vector (IV)
                            prepended to the ciphertext.
        key (bytes): The 16, 24, or 32-byte decryption key for AES.

    Returns:
        bytes: The decrypted data in bytes format.
    """
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_message) + unpadder.finalize()
