import pickle

from src.crypto.hashing import hash_sha256
from src.crypto.placeholder import dummy_decrypt_fernet
from src.crypto.placeholder import dummy_encrypt_fernet
from src.exceptions.encryption_exception import EncryptionException


class Password:
    def __init__(self, password: str):
        """
        Initializes a new Password instance.

        Args:
            password (str): The password to be stored, in plaintext.
        """
        self.is_encrypted: bool = False
        self.password_bytes: bytes = password.encode()
        self.is_master = False

    def encrypt(self, key: bytes) -> None:
        """
        Encrypts the password using the provided key.

        Args:
            key (bytes): The encryption key.

        Raises:
            EncryptionException: If the password is a master password or is
            already encrypted.
        """
        _ = key
        if self.is_master:
            raise EncryptionException("Master password can't be encrypted")
        if self.is_encrypted:
            return
        self.is_encrypted = True
        self._encrypt_password()

    def decrypt(self, key: bytes) -> None:
        """
        Decrypts the password using the provided key.

        Args:
            key (bytes): The decryption key.

        Raises:
            EncryptionException: If the password is a master password or is not
            encrypted.
        """
        _ = key
        if self.is_master:
            raise EncryptionException("Master password can't be decrypted")
        if not self.is_encrypted:
            return
        self.is_encrypted = False
        self._decrypt_password()

    def _encrypt_password(self) -> None:
        """
        Performs the actual encryption of the password.
        """
        self.password_bytes = dummy_encrypt_fernet(self.password_bytes)

    def _decrypt_password(self) -> None:
        """
        Performs the actual decryption of the password.
        """
        self.password_bytes = dummy_decrypt_fernet(self.password_bytes)

    def make_master(self) -> None:
        """
        Marks the password as a master password by hashing it.

        Raises:
            ValueError: If the password is already a master password or is
            encrypted.
        """
        if self.is_master:
            raise ValueError("Password is already master")
        if self.is_encrypted:
            raise ValueError("Password is encrypted")

        self.password_bytes = hash_sha256(self.password_bytes)
        self.is_master = True

    def __call__(self) -> bytes:
        """
        Returns the current password value.

        Returns:
            bytes: The password in its current form (encrypted or plaintext).
        """
        return self.password_bytes


def adapt_password(password: Password) -> bytes:
    """
    Serializes the Password instance to a bytes object.

    Args:
        password (Password): The Password instance to be serialized.

    Returns:
        bytes: The serialized Password instance.

    Raises:
        TypeError: If the Password instance is neither encrypted nor a master
        password.
    """
    if not password.is_encrypted and not password.is_master:
        raise TypeError("Password is not encrypted")

    return pickle.dumps(password)


def convert_password(password: bytes) -> Password:
    """
    Deserializes a bytes object to a Password instance.

    Args:
        password (bytes): The serialized Password instance.

    Returns:
        Password: The deserialized Password instance.

    Raises:
        TypeError: If the deserialized object is not a Password instance.
    """
    retrieved_password: Password = pickle.loads(password)
    if not isinstance(retrieved_password, Password):
        raise TypeError("Password expected")
    return retrieved_password
