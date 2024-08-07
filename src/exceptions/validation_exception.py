class ValidationException(Exception):
    def __init__(self, message: str = "Validation Exception") -> None:
        self.message = message
        super().__init__(message)
