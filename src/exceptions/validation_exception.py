"""
Exception raised for validation errors, such as invalid input data or failed checks.
"""
class ValidationException(Exception):
    """
    Exception raised for errors related to validation operations.

    This exception is used to indicate issues that occur during validation
    processes, such as invalid input data or failed validation checks.

    Args:
        message (str, optional): An optional error message describing the specific
        validation-related error. Defaults to "Validation Exception".

    Attributes:
        message (str): The error message associated with the exception.
    """
    def __init__(self, message: str = "Validation Exception") -> None:
        """
        Initializes the ValidationException with an optional error message.

        Args:
            message (str, optional): An optional error message describing the specific
            validation-related error. Defaults to "Validation Exception".

        """
        self.message = message
        super().__init__(message)
