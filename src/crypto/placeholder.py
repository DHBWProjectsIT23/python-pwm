from cryptography.fernet import Fernet

KEY = b"NsnezLc_TNwg9XFD3roUsS-Wd9jbGKRln7-kGtCw2nM="


def dummy_encrypt_fernet(data: bytes) -> bytes:
    """
    Encrypts the given data using the Fernet symmetric encryption.

    Args:
        data (bytes): The data to be encrypted.

    Returns:
        bytes: The encrypted data, including the encryption metadata.
    """
    f = Fernet(KEY)
    return f.encrypt(data)


def dummy_decrypt_fernet(data: bytes) -> bytes:
    """
    Decrypts the given encrypted data using the Fernet symmetric encryption.

    Args:
        data (bytes): The encrypted data to be decrypted.

    Returns:
        bytes: The decrypted data.
    """
    f = Fernet(KEY)
    return f.decrypt(data)


# def encrypt_password_aes256(password: bytes) -> tuple[bytes, CipherContext]:
#     """
#     PLACEHOLDER WITH CHAT-GPT - MIGHT NOT BE CORRECT!
#     """
#     print(f"Password: {password.hex()}")
#
#     # random key 265-bit (32-byte)
#     key = os.urandom(32)
#     print(f"Key: {key.hex()}")
#
#     # random 128-bit (16 byte) IV
#     iv = os.urandom(16)
#     print(f"IV: {iv.hex()}")
#
#     # pad password to be multiple of block size (16 byte)
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_password = padder.update(password) + padder.finalize()
#     print(f"Padded password: {padded_password.hex()}")
#
#     # cypher using key and IV
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#
#     # create encryptor object
#     encryptor = cipher.encryptor()
#
#     # perform encryption
#     encrypted_password = encryptor.update(padded_password) + encryptor.finalize()
#     print(f"Ciphertext: {encrypted_password.hex()}")
#
#     return encrypted_password, cipher.decryptor()
#
#
# def decrypt_password_aes256(decryptor: CipherContext, encrypted_password: bytes) -> str:
#     """
#     PLACEHOLDER WITH CHAT-GPT - MIGHT NOT BE CORRECT!
#     """
#     decrypted_padded_password = (
#         decryptor.update(encrypted_password) + decryptor.finalize()
#     )
#
#     unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#     decrypted_password = (
#         unpadder.update(decrypted_padded_password) + unpadder.finalize()
#     )
#
#     print(f"Decrypted Password: {decrypted_password}")
#     return decrypted_password.decode()
