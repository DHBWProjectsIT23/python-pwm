from typing import TypedDict


class RequiredPasswordDict(TypedDict):
    """
    A dictionary that represents required password information.

    Keys:
        current_password (str): The current password.
    """

    current_password: str


class OptionalPasswordDict(TypedDict, total=False):
    """
    A dictionary that represents optional password information.

    Keys:
        old_passwords (list[str]): A list of old passwords.
    """

    old_passwords: list[str]


class PasswordDict(RequiredPasswordDict, OptionalPasswordDict):
    """
    A dictionary that represents both required and optional password
    information.

    Inherits:
        RequiredPasswordDict: Contains the required password key.
        OptionalPasswordDict: Contains optional old_passwords key.
    """


class RequiredPasswordInformationDict(TypedDict):
    """
    A dictionary that represents required password information details.

    Keys:
        description (str): A description of the password information.
        password (PasswordDict): A dictionary containing password information.
    """

    description: str
    password: PasswordDict


class OptionalPasswordInformationDict(TypedDict, total=False):
    """
    A dictionary that represents optional password information details.

    Keys:
        username (str): The username associated with the password.
        categories (list[str]): A list of categories for the password.
        note (str): Additional notes about the password.
        created_at (float): The timestamp when the password information was
            created.
        last_modified (float): The timestamp when the password information was
            last modified.
    """

    username: str
    categories: list[str]
    note: str
    created_at: float
    last_modified: float


class PasswordInformationDict(
    RequiredPasswordInformationDict, OptionalPasswordInformationDict
):
    """
    A dictionary that represents both required and optional password information
    details.

    Inherits:
        RequiredPasswordInformationDict: Contains the required details for
            password information.
        OptionalPasswordInformationDict: Contains optional details for password
            information.
    """
