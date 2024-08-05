class EncryptionException(Exception):
    def __init__(self, message: str = "Encryption Exception") -> None:
        self.message = message
        super().__init__(message)
