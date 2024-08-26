"""
Provides functions to export `PasswordInformation` objects to a JSON file, 
including conversion to dictionaries and file writing with optional timestamp-based filenames.
"""
import json
from datetime import datetime
from typing import Optional

from src.import_export.password_dict import PasswordInformationDict
from src.model.password_information import PasswordInformation


def _convert_to_dict(
    password_informations: list[PasswordInformation],
) -> list[PasswordInformationDict]:
    """
    Converts a list of PasswordInformation objects to a list of dictionaries.

    Args:
        password_informations (List[PasswordInformation]): The list of PasswordInformation
        objects to convert.

    Returns:
        List[PasswordInformationDict]: A list of dictionaries representing the
        PasswordInformation objects.

    Notes:
        Each PasswordInformation object is converted to a dictionary using its
        `to_dict` method. The resulting list of dictionaries can be serialized to JSON format.
    """
    return [pw_info.to_dict() for pw_info in password_informations]


def export_to_json(
    password_informations: list[PasswordInformation],
    target_file: Optional[str] = None,
) -> str:
    """
    Exports a list of PasswordInformation objects to a JSON file.

    Args:
        password_informations (List[PasswordInformation]): The list of PasswordInformation
        objects to export.
        target_file (Optional[str], optional): The path of the target JSON file.
        If None, a default filename with the current timestamp will be used. Defaults to None.

    Returns:
        str: The path of the exported JSON file.

    Raises:
        IOError: If an error occurs while writing to the file.

    Notes:
        - If `target_file` is not provided, the filename will include a placeholder
          for the current timestamp (e.g., `export_ddmmyyHHMM.json`).
        - The file will be written with UTF-8 encoding.
    """
    dicts = _convert_to_dict(password_informations)
    if target_file is None:
        current_timestamp = datetime.now().strftime("%d%m%y%H%M")
        target_file = f"export_{current_timestamp}.json"
    with open(target_file, "w", encoding="utf-8") as file:
        json.dump(dicts, file, indent=2)

    return target_file
