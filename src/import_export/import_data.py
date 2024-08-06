import json
from src.exceptions.import_exception import ImportException
from src.import_export.password_dict import PasswordDict, PasswordInformationDict
from src.model.password_information import PasswordInformation
from src.model.user import User


def import_json(target_file: str, user: User) -> list[PasswordInformation]:
    with open(target_file, "r") as file:
        try:
            data_list: list[PasswordInformationDict] = json.load(file)
        except json.JSONDecodeError as e:
            raise ImportException(f"{e.msg} in line {e.lineno}")
        verify_required_key(data_list)
        check_invalid_keys(data_list)
        return [PasswordInformation.from_dict(item, user) for item in data_list]


def verify_required_key(data_list: list[PasswordInformationDict]) -> None:
    required_keys = PasswordInformationDict.__required_keys__
    password_required_keys = PasswordDict.__required_keys__
    for i, item in enumerate(data_list):
        missing_keys = required_keys - item.keys()
        if len(missing_keys) != 0:
            raise ImportException(f"Item {i+1} is missing keys {missing_keys}")

        missing_password_keys = password_required_keys - item["password"].keys()
        if len(missing_password_keys) != 0:
            raise ImportException(
                f"Item {i+1} is missing password keys {missing_password_keys}"
            )


def check_invalid_keys(data_list: list[PasswordInformationDict]) -> None:
    allowed_keys = (
        PasswordInformationDict.__required_keys__
        | PasswordInformationDict.__optional_keys__
    )
    allowed_password_keys = (
        PasswordDict.__required_keys__ | PasswordDict.__optional_keys__
    )

    for i, item in enumerate(data_list):
        invalid_keys = item.keys() - allowed_keys
        if len(invalid_keys) != 0:
            raise ImportException(f"Item {i+1} contains invalid keys {invalid_keys}")

        invalid_password_keys = item["password"].keys() - allowed_password_keys
        if len(invalid_password_keys) != 0:
            raise ImportException(
                f"Item {i+1} contains invalid password keys {invalid_password_keys}"
            )
