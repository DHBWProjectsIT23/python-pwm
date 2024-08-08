import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def encrypt_aes(data: str, key: bytes) -> bytes:
    """
    Encrypts the data using the provided key.

    Args:
        data (str): The data to be decrypted.
        key (bytes): The encryption key.
    """
    iv = os.urandom(16)
    padder: padding.PaddingContext = padding.PKCS7(128).padder()
    padded_message: bytes = padder.update(data.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return iv + ciphertext


def decrypt_aes(ciphertext: bytes, key: bytes) -> bytes:
    """
    Decrypts the data using the provided key.

    Args:
        ciphertext (bytes): The encrypted data to be decrypted
        key (bytes): The key used for the encryption:
    """
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_message) + unpadder.finalize()
