# pylint: disable=E1101
# Appears to be bugged, changes were recently merged for astroid 3.3.0
# However as of now 3.2.4 is used
# Reference:
#   Pylint issue: https://github.com/pylint-dev/pylint/issues/7126
#   Astroid pull request: https://github.com/pylint-dev/astroid/pull/2431
#   Pylint Documentation:
#       https://pylint.readthedocs.io/en/latest/user_guide/messages/error/no-member.html
import json

from src.exceptions.import_exception import ImportException
from src.import_export.password_dict import PasswordDict
from src.import_export.password_dict import PasswordInformationDict
from src.model.password_information import PasswordInformation
from src.model.user import User


def import_json(target_file: str, user: User) -> list[PasswordInformation]:
    """
    Imports password information from a JSON file and converts it to a list of
    PasswordInformation objects.

    Args:
        target_file (str): The path to the JSON file to import.
        user (User): The user associated with the imported password information.

    Returns:
        list[PasswordInformation]: A list of PasswordInformation objects created
        from the JSON data.

    Raises:
        ImportException: If there is an error in the JSON format or if required
        keys are missing or invalid.
    """
    with open(target_file, "r", encoding="utf-8") as file:
        try:
            data_list: list[PasswordInformationDict] = json.load(file)
        except json.JSONDecodeError as e:
            raise ImportException(f"{e.msg} in line {e.lineno}") from e
        verify_required_key(data_list)
        check_invalid_keys(data_list)
        return [PasswordInformation.from_dict(item, user) for item in data_list]


def verify_required_key(data_list: list[PasswordInformationDict]) -> None:
    """
    Verifies that all required keys are present in each item of the imported
    JSON data.

    Args:
        data_list (list[PasswordInformationDict]): The list of dictionaries
        representing password information.

    Raises:
        ImportException: If any item is missing required keys or if password
        keys are missing.
    """
    required_keys = PasswordInformationDict.__required_keys__
    password_required_keys = PasswordDict.__required_keys__
    for i, item in enumerate(data_list):
        missing_keys = required_keys - item.keys()
        if len(missing_keys) != 0:
            raise ImportException(f"Item {i + 1} is missing keys {missing_keys}")

        missing_password_keys = password_required_keys - item["password"].keys()
        if len(missing_password_keys) != 0:
            raise ImportException(
                f"Item {i + 1} is missing password keys {missing_password_keys}"
            )


def check_invalid_keys(data_list: list[PasswordInformationDict]) -> None:
    """
    Checks that all keys in the imported JSON data are valid, according to the
    allowed keys.

    Args:
        data_list (list[PasswordInformationDict]): The list of dictionaries
        representing password information.

    Raises:
        ImportException: If any item contains invalid keys or if password keys
        are invalid.
    """
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
            raise ImportException(f"Item {i + 1} contains invalid keys {invalid_keys}")

        invalid_password_keys = item["password"].keys() - allowed_password_keys
        if len(invalid_password_keys) != 0:
            raise ImportException(
                f"""Item {i + 1} contains invalid password keys
                {invalid_password_keys}""".replace(
                    "\n", " "
                )
            )
