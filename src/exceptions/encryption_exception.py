class EncryptionException(Exception):
    """
    Exception raised for errors related to encryption operations.

    Args:
        message (str, optional): An optional error message. Defaults to "Encryption Exception".

    Attributes:
        message (str): The error message associated with the exception.
    """
    def __init__(self, message: str = "Encryption Exception") -> None:
        self.message = message
        super().__init__(message)
