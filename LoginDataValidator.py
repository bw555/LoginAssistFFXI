import json
import typing
import xml.etree.ElementTree as ET

from LoginData import LoginData
from CustomExceptions import (
    PlayonlineIDFormatException,
    InvalidOneTimePasswordException,
    RepeatedMemberException,
    MemberNotADigitException,
)


def parse_login_data() -> list[LoginData]:
    login_data_list: list[LoginData] = list()

    with open(r'./data/login_data.json', 'r') as f:
        accountsList: list[dict[str, str | bool]] = json.load(f)

    for account in accountsList:
        login_data_list.append(
            LoginData(
                character_name=account['character_name'],
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


def parse_login_data_xml() -> list[LoginData]:
    tree = ET.parse('./data/login_data.xml')
    accounts_xml = tree.getroot()
    login_data_list = []
    for account in accounts_xml.findall('account'):
        data = LoginData(*(['N/A'] * 8))
        profiles = set()
        for xml_tag in account:
            if xml_tag.tag == 'windower_profile':
                profiles.add(xml_tag.text)
            else:
                data.__setattr__(xml_tag.tag, xml_tag.text)

        data.__setattr__('windower_profile', profiles)
        data.onetimepassword_enabled = validate_onetimepassword(
            account.find('onetimepassword_enabled').text
        )

        data.member = int(data.member)

        login_data_list.append(data)

    validate_member_values(login_data_list)
    validate_playonline_id(login_data_list)
    return login_data_list


def validate_onetimepassword(otp: str) -> None | bool:
    otp = otp.lower()
    if otp in {'t', 'true'}:
        return True
    elif otp in {'f', 'false'}:
        return False
    else:
        raise InvalidOneTimePasswordException('Possible values are: t, true, f, false')


def gather_windower_profiles(accounts: list[LoginData]) -> dict[str, list[LoginData]]:
    profile_charnames = dict() # Key is profile name, value is login data

    for account in accounts:
        for profile in account.windower_profile:
            if profile in profile_charnames:
                profile_charnames[profile].append(account)
            else:
                profile_charnames[profile] = [account]

    return profile_charnames


# This could be improved TODO
def get_requested_accounts(profile_or_char_name: str) -> list[LoginData]:
    all_accounts = parse_login_data_xml()
    login_accounts = []
    for account in all_accounts:
        if account.character_name == profile_or_char_name:
            login_accounts.append(account)
        elif profile_or_char_name in account.windower_profile:
            login_accounts.append(account)
    return login_accounts


def gather_charnames(accounts: list[LoginData]) -> set[str]:
    names = set()
    for account in accounts:
        names.add(account.character_name)
    return names


def validate_playonline_id(login_data: list[LoginData]) -> None:
    # Playonline ID has 4 capital letters followed by 4 digits
    for account in login_data:
        if len(account.playonline_id) != 8:
            raise PlayonlineIDFormatException(
                account.character_name,
                f'Incorrect length of {len(account.playonline_id)}, expected 8',
            )
        for letter in account.playonline_id[:4]:
            if not letter.isupper():
                raise PlayonlineIDFormatException(
                    account.character_name,
                    f'First 4 characters in playonline id must be capital letters',
                )
        for digit in account.playonline_id[4:]:
            if not digit.isdigit():
                raise PlayonlineIDFormatException(
                    account.character_name,
                    f'Last 4 characters in playonline id must be digits',
                )


def validate_member_values(accounts: list[LoginData]) -> None:
    valid_member_values = {0, 1, 2, 3}
    used_values: dict[int, str] = {}

    for account in accounts:
        try:
            int(account.member)
        except ValueError as ve:
            raise MemberNotADigitException(
                f'{account.character_name} has an invalid value for member, {account.member} should be a digit.'
            )

        if (
            int(account.member) in valid_member_values
            and int(account.member) not in used_values
        ):
            used_values[int(account.member)] = account.character_name
        elif (
            int(account.member) in valid_member_values
            and int(account.member) in used_values
        ):
            raise RepeatedMemberException(
                f'Accounts cannot have the same member value, {account.character_name} and {used_values[int(account.member)]} have the same member value'
            )
