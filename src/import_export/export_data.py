from datetime import datetime
import json
from typing import Optional
from src.model.password_information import PasswordInformation
from .password_dict import PasswordInformationDict


def _convert_to_dict(
    password_informations: list[PasswordInformation],
) -> list[PasswordInformationDict]:
    return [pw_info.to_dict() for pw_info in password_informations]


def export_to_json(
    password_informations: list[PasswordInformation],
    target_file: Optional[str] = None,
) -> str:
    dicts = _convert_to_dict(password_informations)
    if target_file is None:
        # current_timestamp = datetime.now().strftime("%d%m%y%H%M")
        current_timestamp = "CHANGE_ME"
        target_file = f"export_{current_timestamp}.json"
    with open(target_file, "w") as file:
        json.dump(dicts, file, indent=2)

    return target_file
