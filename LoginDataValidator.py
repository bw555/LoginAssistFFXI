import json
import typing
import xml
from LoginData import LoginData
from CustomExceptions import PlayonlineIDFormatException


def parse_login_data() -> list[LoginData]:
    login_data_list: list[LoginData] = list()

    with open(r'./data/login_data.json', 'r') as f:
        accountsList: list[dict[str, str | bool]] = json.load(f)

    for account in accountsList:
        login_data_list.append(
            LoginData(
                char_name=account['character_name'],
                playonline_id=account['playonline_id'],
                playonline_password=account['playonline_password'],
                square_enix_id=account['square_enix_id'],
                square_enix_password=account['square_enix_password'],
                onetimepassword_enabled=account['onetimepassword_enabled'],
                guest=account['guest'],
            )
        )

    validate_playonline_id(login_data_list)

    return login_data_list


def validate_playonline_id(login_data: list[LoginData]) -> None:
    # Playonline ID has 4 capital letters followed by 4 digits
    for account in login_data:
        if len(account.playonline_id) != 8:
            raise PlayonlineIDFormatException(
                account.char_name,
                f'Incorrect length of {len(account.playonline_id)}, expected 8',
            )
        for letter in account.playonline_id[:4]:
            if not letter.isupper():
                raise PlayonlineIDFormatException(
                    account.char_name,
                    f'First 4 characters in playonline id must be capital letters',
                )
        for digit in account.playonline_id[4:]:
            if not digit.isdigit():
                raise PlayonlineIDFormatException(
                    account.char_name,
                    f'Last 4 characters in playonline id must be digits',
                )
