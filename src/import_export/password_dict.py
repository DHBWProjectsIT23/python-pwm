from typing import TypedDict


class RequiredPasswordDict(TypedDict):
    current_password: str


class OptionalPasswordDict(TypedDict, total=False):
    old_passwords: list[str]


class PasswordDict(RequiredPasswordDict, OptionalPasswordDict):
    pass


class RequiredPasswordInformationDict(TypedDict):
    description: str
    password: PasswordDict


class OptionalPasswordInformationDict(TypedDict, total=False):
    username: str
    categories: list[str]
    note: str
    created_at: float
    last_modified: float


class PasswordInformationDict(
    RequiredPasswordInformationDict, OptionalPasswordInformationDict
):
    pass
