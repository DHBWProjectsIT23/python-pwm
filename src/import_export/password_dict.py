from typing import NotRequired
from typing import Required
from typing import TypedDict


class PasswordDict(TypedDict):
    current_password: Required[str]
    old_passwords: NotRequired[list[str]]


class PasswordInformationDict(TypedDict):
    description: Required[str]
    password: Required[PasswordDict]
    username: NotRequired[str]
    categories: NotRequired[list[str]]
    note: NotRequired[str]
    created_at: NotRequired[float]
    last_modified: NotRequired[float]
