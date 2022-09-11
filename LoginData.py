from dataclasses import dataclass


@dataclass
class LoginData:

    char_name: str
    playonline_id: str
    playonline_password: str
    square_enix_id: str
    square_enix_password: str
    onetimepassword_enabled: bool
    guest: bool
