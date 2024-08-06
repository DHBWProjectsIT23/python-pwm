class ExitFromTextBoxException(Exception):
    """
    Exception raised when an error occurs related to exiting or handling a text box.

    Args:
        message (str, optional): An optional error message. Defaults to an empty string.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(message)
