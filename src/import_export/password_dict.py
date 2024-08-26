"""
Defines `TypedDict` classes for representing password and detailed password information.
"""
from typing import NotRequired
from typing import Required
from typing import TypedDict


class PasswordDict(TypedDict):
    """
    Represents a dictionary containing password information.

    Args:
        current_password (Required[str]): The current password.
        old_passwords (NotRequired[list[str]]): A list of old passwords (optional).
    """
    current_password: Required[str]
    old_passwords: NotRequired[list[str]]


class PasswordInformationDict(TypedDict):
    """
    Represents a dictionary containing detailed password information.

    Args:
        description (Required[str]): A description for the password information.
        password (Required[PasswordDict]): A dictionary with current and old passwords.
        username (NotRequired[str]): The username associated with the password (optional).
        categories (NotRequired[list[str]]): 
        A list of categories or tags for the password (optional).
        note (NotRequired[str]): Additional notes about the password (optional).
        created_at (NotRequired[float]): 
        The timestamp when the password information was created (optional).
        last_modified (NotRequired[float]): 
        The timestamp when the password information was last modified (optional).
    """
    description: Required[str]
    password: Required[PasswordDict]
    username: NotRequired[str]
    categories: NotRequired[list[str]]
    note: NotRequired[str]
    created_at: NotRequired[float]
    last_modified: NotRequired[float]
