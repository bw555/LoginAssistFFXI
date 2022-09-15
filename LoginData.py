from dataclasses import dataclass

VALID_MEMBER_VALS = {0, 1, 2, 3}


@dataclass
class LoginData:

    char_name: str
    playonline_id: str
    playonline_password: str
    square_enix_id: str
    square_enix_password: str
    windower_profile: str
    onetimepassword_enabled: bool
    member: int
