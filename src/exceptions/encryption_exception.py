"""
This module defines the `EncryptionException` class used 
to handle errors related to encryption operations.

The `EncryptionException` class provides a custom exception for 
signaling issues that occur during encryption or decryption processes.
"""


class EncryptionException(Exception):
    """
    Exception raised for errors related to encryption operations.

    This exception can be used to indicate issues that occur during encryption
    or decryption processes.

    Args:
        message (str, optional): An optional error message. Defaults to
        "Encryption Exception".

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message: str = "Encryption Exception") -> None:
        """
        Initializes the EncryptionException with an optional error message.

        Args:
            message (str, optional): An optional error message. Defaults to
            "Encryption Exception".
        """
        self.message = message
        super().__init__(message)
