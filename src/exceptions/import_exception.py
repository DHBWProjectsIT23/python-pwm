"""
This module defines the `ImportException` class used to handle errors related to import operations.

The `ImportException` class provides a custom exception for signaling issues 
that occur during import operations, such as failures in loading or processing imported data.
"""
class ImportException(Exception):
    """
    Exception raised for errors related to import operations.

    This exception is used to indicate errors that occur during import operations,
    such as failures in loading or processing imported data.

    Args:
        message (str, optional): An optional error message describing the specific
        import-related error. Defaults to "Import Exception".

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message: str = "Import Exception") -> None:
        """
        Initializes the ImportException with an optional error message.

        Args:
            message (str, optional): An optional error message describing the specific
            import-related error. Defaults to "Import Exception".
        """
        self.message = message
        super().__init__(message)
