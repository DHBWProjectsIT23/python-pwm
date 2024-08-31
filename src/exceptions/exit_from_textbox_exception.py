"""
This module defines the `ExitFromTextBoxException` class used to handle 
errors related to exiting or handling a text box component.

The `ExitFromTextBoxException` class provides a custom exception for signaling 
issues that occur when interacting with or exiting from a text box.
"""
class ExitFromTextBoxException(Exception):
    """
    Exception raised when an error occurs related to exiting or handling a
    text box.

    This exception is used to indicate errors that occur when interacting with
    or exiting from a text box component.

    Args:
        message (str, optional): An optional error message describing the error.
        Defaults to an empty string.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message: str = "") -> None:
        """
        Initializes the ExitFromTextBoxException with an optional error message.

        Args:
            message (str, optional): An optional error message describing the error.
            Defaults to an empty string.
        """
        self.message = message
        super().__init__(message)
