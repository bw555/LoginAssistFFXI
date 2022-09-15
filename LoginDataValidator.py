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
                windower_profile=account['windower_profile'],
                onetimepassword_enabled=account['onetimepassword_enabled'],
                member=account['member'],
            )
        )

    validate_playonline_id(login_data_list)

    return login_data_list


def gather_windower_profiles(accounts: list[LoginData]) -> dict[str, list[LoginData]]:
    profile_charnames = dict()

    for account in accounts:
        if account.windower_profile in profile_charnames:
            profile_charnames[account.windower_profile].append(account)
        else:
            profile_charnames[account.windower_profile] = [account]

    return profile_charnames


# This could be improved TODO
def get_requested_accounts(profile_or_char_name: str) -> list[LoginData]:
    all_accounts = parse_login_data()
    login_accounts = []
    for account in all_accounts:
        if account.char_name == profile_or_char_name:
            login_accounts.append(account)
        elif account.windower_profile == profile_or_char_name:
            login_accounts.append(account)
    return login_accounts


def gather_charnames(accounts: list[LoginData]) -> set[str]:
    names = set()
    for account in accounts:
        names.add(account.char_name)
    return names


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
