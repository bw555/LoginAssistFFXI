from typing import Final

GUEST_LOGIN: Final[tuple[int, int]] = (315, 343)
PLAYONLINE_ID_LOGIN: Final[tuple[int, int]] = (969, 409)
PLAYONLINE_PASSWORD_OPEN: Final[tuple[int, int]] = (975, 452)
PLAYONLINE_PASSWORD_CLOSE: Final[tuple[int, int]] = (691, 345)
SQUARE_ENIX_ID_LOGIN: Final[tuple[int, int]] = (981, 569)
GUEST_LOGIN_OK_BUTTON: Final[tuple[int, int]] = (866, 692)
LOGIN_INFO_LOGIN_BUTTON: Final[tuple[int, int]] = (248, 365)
SQUARE_ENIX_PASSWORD_OPEN: Final[tuple[int, int]] = (969, 454)

FIRST_MEMBER_LOGIN_POS: Final[tuple[int, int]] = (862, 324)
SECOND_MEMBER_LOGIN_POS: Final[tuple[int, int]] = (862, 424)
THIRD_MEMBER_LOGIN_POS: Final[tuple[int, int]] = (862, 520)
FOURTH_MEMBER_LOGIN_POS: Final[tuple[int, int]] = (862, 666)
MEMBER_LOGIN_POSITIONS_LIST: Final[tuple[int, int]] = [
    FIRST_MEMBER_LOGIN_POS,
    SECOND_MEMBER_LOGIN_POS,
    THIRD_MEMBER_LOGIN_POS,
    FOURTH_MEMBER_LOGIN_POS,
]

ONE_TIME_GUEST_TOGGLE_BOX: Final[tuple[int, int]] = (853, 624)
ONE_TIME_GUEST_ENABLE_BOX: Final[tuple[int, int]] = (921, 676)

SQUARE_ENIX_PASSWORD_CLOSE: Final[tuple[int, int]] = (699, 343)
CONNECT_BUTTON: Final[tuple[int, int]] = (407, 606)

ONE_TIME_PASSWORD_BOX: Final[tuple[int, int]] = (975, 507)

SCROLL_START: Final[tuple[int, int]] = (1246, 454)
SCROLL_END: Final[tuple[int, int]] = (1246, 798)
NOTICE_ACCEPT_BUTTON: Final[tuple[int, int]] = (760, 835)
MAIL_INFO_BUTTON: Final[tuple[int, int]] = (999, 635)

FFXI_BUTTON: Final[tuple[int, int]] = (277, 365)
PLAY_BUTTON: Final[tuple[int, int]] = (352, 212)
PLAY_BUTTON_SECOND: Final[tuple[int, int]] = (477, 803)
MAINTENANCE_CLOSE_BUTTON: Final[tuple[int, int]] = (160, 773)

WINDOW_WIDTH: Final[int] = 1400
WINDOW_HEIGHT: Final[int] = 1000

IMG_REGION_PLAYONLINE: Final[tuple[int, int, int, int]] = (
    0,
    0,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
FFXI_RESOLUTION: Final[tuple[int, int]] = (1920, 1080)
IMG_REGION_FFXI: Final[tuple[int, int, int, int]] = (0, 0, *FFXI_RESOLUTION)

CHARACTER_SELECT_SECOND: Final[tuple[int, int]] = (1655, 850)
CHARACTER_SELECT_THIRD: Final[tuple[int, int]] = (962, 570)

EMERGENCY_EXIT_WINDOW_WIDTH: Final[int] = 400
EMERGENCY_EXIT_WINDOW_HEIGHT: Final[int] = 200
