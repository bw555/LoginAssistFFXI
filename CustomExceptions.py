from dataclasses import dataclass


@dataclass
class MissingPlayonlineWindowException(Exception):
    window_count: int
    account_count: int


@dataclass
class TimeoutException(Exception):
    msg: str


@dataclass
class PlayonlineIDFormatException(Exception):
    char_name: str
    msg: str


@dataclass
class EmergencyExitException(Exception):
    msg: str


@dataclass
class InvalidProfileException(Exception):
    msg: str
