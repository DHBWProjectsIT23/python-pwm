class ImportException(Exception):
    """
    Exception raised for errors related to import operations.

    Args:
        message (str, optional): An optional error message. Defaults to "Import Exception".

    Attributes:
        message (str): The error message associated with the exception.
    """
    def __init__(self, message: str = "Import Exception") -> None:
        self.message = message
        super().__init__(message)
