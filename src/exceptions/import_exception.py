class ImportException(Exception):
    def __init__(self, message: str = "Import Exception") -> None:
        self.message = message
        super().__init__(message)
