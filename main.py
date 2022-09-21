# pyinstaller --noconfirm --onefile --console main.py --distpath "./" -n "LoginAssistFFXI"
from typing import Callable, Any
import pyautogui as ag
import pygetwindow as gw
import sys
import cv2

import PIL

from LoginData import LoginData, VALID_MEMBER_VALS
from CustomExceptions import MissingPlayonlineWindowException, TimeoutException
import LoginDataValidator
import PositionConstants

import asyncio
import logging
import time
from dataclasses import dataclass

from ProfileSelectBox import ProfileSelectBox

login_logger = logging.getLogger(__name__)
login_logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(
    '%(levelname)s %(name)s %(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(message)s',
    datefmt='%d-%b-%Y %I:%M:%S%p',
)
log_handler = logging.FileHandler('./debug.log')
log_handler.setFormatter(log_formatter)
login_logger.addHandler(log_handler)

ag.FAILSAFE = True  # Move mouse to upper-left to abort program


WindowType = gw._pygetwindow_win.Win32Window

primary_monitor_res: tuple[int, int] = ag.size()


def find_playonline_windows(
    accounts_list: list[LoginData], enable_exception: bool = True
) -> list[WindowType]:
    PLAYONLINE_START = 'PlayOnline Viewer'
    titles = [x for x in gw.getAllTitles() if x.startswith(PLAYONLINE_START)]
    if len(titles) != len(accounts_list) and enable_exception:
        raise MissingPlayonlineWindowException(
            window_count=len(titles), account_count=len(accounts_list)
        )
    windows = [
        window
        for window in gw.getWindowsWithTitle(PLAYONLINE_START)
        if window.title.startswith(PLAYONLINE_START)
    ]
    login_logger.debug(windows)

    return windows


async def move_and_resize_windows(
    windows: list[WindowType],
    width: int = PositionConstants.WINDOW_WIDTH,
    height: int = PositionConstants.WINDOW_HEIGHT,
) -> list[tuple[int, int]]:
    login_logger.debug(f'Resizing and moving windows')
    window_dimensions = []
    for window in windows:
        window_dimensions.append(window.size)
        window.moveTo(0, 0)
        window.resizeTo(width, height)

    return window_dimensions


async def playonline_login(account: LoginData) -> None:

    if account.member not in VALID_MEMBER_VALS:
        login_logger.debug(f'Starting playonline login process on: guest')
        ag.leftClick(*PositionConstants.GUEST_LOGIN)
        await asyncio.sleep(0.5)
        ag.leftClick(*PositionConstants.PLAYONLINE_ID_LOGIN)
        await asyncio.sleep(0.5)
        ag.typewrite(account.playonline_id)
        login_logger.debug(f'Entered PlayonlineID for guest')

        ag.leftClick(*PositionConstants.PLAYONLINE_PASSWORD_OPEN)
        ag.leftClick(*PositionConstants.PLAYONLINE_PASSWORD_CLOSE)
        await asyncio.sleep(0.5)
        ag.typewrite(account.playonline_password)
        ag.typewrite(['enter'] * 2, interval=0.01)
        ag.moveTo(*PositionConstants.SQUARE_ENIX_ID_LOGIN)
        login_logger.debug(f'Entered PlayonlinePassword for guest')

        await asyncio.sleep(1)

        ag.doubleClick(*PositionConstants.SQUARE_ENIX_ID_LOGIN)
        ag.typewrite(account.square_enix_id)

        login_logger.debug(f'Entered SquareEnixID for guest')
        if account.onetimepassword_enabled:
            # await asyncio.sleep(0.5)
            ag.moveTo(*PositionConstants.ONE_TIME_GUEST_TOGGLE_BOX)
            ag.leftClick()
            # await asyncio.sleep(0.1)
            ag.moveTo(*PositionConstants.ONE_TIME_GUEST_ENABLE_BOX)
            ag.leftClick()

        ag.leftClick(*PositionConstants.GUEST_LOGIN_OK_BUTTON)

        await asyncio.sleep(0.7)

        ag.leftClick(*PositionConstants.LOGIN_INFO_LOGIN_BUTTON)
        ag.moveTo(*PositionConstants.SQUARE_ENIX_PASSWORD_OPEN)

        await asyncio.sleep(1)

        ag.leftClick(*PositionConstants.SQUARE_ENIX_PASSWORD_OPEN)
        await asyncio.sleep(0.5)
        ag.leftClick(*PositionConstants.SQUARE_ENIX_PASSWORD_CLOSE)
        await asyncio.sleep(0.5)
        ag.typewrite(account.square_enix_password)
        await asyncio.sleep(2)
        ag.typewrite(['enter'] * 2, interval=0.1)
        login_logger.debug(f'Entered SquareEnixID for guest')

        if account.onetimepassword_enabled:
            await asyncio.sleep(3)
            onetime_password = ag.prompt(f'Enter guest one time password here:')
            await enter_onetimepassword(onetime_password)
        else:
            await asyncio.sleep(2)

        ag.moveTo(*PositionConstants.CONNECT_BUTTON)
        await asyncio.sleep(0.1)
        ag.leftClick()
        login_logger.debug(f'Ending playonline login process on: guest')
    else:
        ag.leftClick(*PositionConstants.MEMBER_LOGIN_POSITIONS_LIST[account.member])
        await asyncio.sleep(0.5)
        ag.leftClick(*PositionConstants.LOGIN_INFO_LOGIN_BUTTON)
        ag.moveTo(*PositionConstants.SQUARE_ENIX_PASSWORD_OPEN)

        await asyncio.sleep(1)

        ag.leftClick(*PositionConstants.SQUARE_ENIX_PASSWORD_OPEN)
        await asyncio.sleep(0.5)
        ag.leftClick(*PositionConstants.SQUARE_ENIX_PASSWORD_CLOSE)
        await asyncio.sleep(0.5)
        ag.typewrite(account.square_enix_password)
        await asyncio.sleep(2)
        ag.typewrite(['enter'] * 2, interval=0.1)

        if account.onetimepassword_enabled:
            await asyncio.sleep(3)
            onetime_password = ag.prompt(f'Enter member one time password here:')
            await enter_onetimepassword(onetime_password)
            login_logger.debug(f'Entered one time password on member')
        else:
            await asyncio.sleep(2)
        ag.moveTo(*PositionConstants.CONNECT_BUTTON)
        await asyncio.sleep(0.1)
        ag.leftClick()


async def enter_onetimepassword(onetime_password: str) -> None:
    ag.moveTo(*PositionConstants.ONE_TIME_PASSWORD_BOX)
    ag.leftClick()

    ag.typewrite(onetime_password)
    await asyncio.sleep(0.2)


async def start_ffxi(windows: list[WindowType], accounts: list[LoginData]) -> None:
    for window, account in zip(windows, accounts):
        login_logger.debug(f'Start FFXI startup on character')
        ag.moveTo(1, 1)
        activate_window(window)
        # This can get caught clicking on something else right after an update!
        ffxi_button = waitout_image(
            './img/crystal.PNG', timeout_duration=10, exception_enable=False
        )
        if ffxi_button:
            ag.leftClick(*ffxi_button)
            login_logger.debug(f'clicked crystal')
        else:
            ffxi_button = waitout_image('./img/FFXIButton.PNG', timeout_duration=30)
            ag.leftClick(*PositionConstants.FFXI_BUTTON)
            login_logger.debug(f'No crystal')

    for window, account in zip(windows, accounts):
        activate_window(window)
        ag.moveTo(1, 1)
        waitout_image('./img/PlayButton.PNG', timeout_duration=25)
        ag.leftClick(*PositionConstants.PLAY_BUTTON)
        # ag.typewrite(['enter'] * 2, interval=1)

    # May be Maintenance alert here, may not be
    for window, account in zip(windows, accounts):
        activate_window(window)
        maintenance_button = waitout_image(
            './img/MaintenanceAlert.PNG', timeout_duration=2, exception_enable=False
        )
        if maintenance_button:
            login_logger.debug('Maintenance Alert ON')
            ag.leftClick(*PositionConstants.MAINTENANCE_CLOSE_BUTTON)
        else:
            login_logger.debug('Maintenance Alert OFF')
            break

    for window, account in zip(windows, accounts):
        activate_window(window)
        ag.moveTo(1, 1)
        waitout_image('./img/PlayButton2.PNG', timeout_duration=25)
        ag.leftClick(*PositionConstants.PLAY_BUTTON_SECOND)
        login_logger.debug(f'Finishing FFXI Startup on character')


def activate_window(window: WindowType) -> None:
    window.activate()
    while not window.isActive:
        pass


async def login_to_playonline(
    playonline_windows: list[WindowType], login_data: list[LoginData]
) -> None:
    for window, account in zip(playonline_windows, login_data):
        activate_window(window)
        await asyncio.sleep(1)
        await playonline_login(account)


async def guest_scroll(account: LoginData) -> None:
    await asyncio.sleep(0.5)
    ag.moveTo(*PositionConstants.SCROLL_START)
    ag.mouseDown(*PositionConstants.SCROLL_START, button='left')
    ag.moveTo(*PositionConstants.SCROLL_END)
    ag.mouseUp(button='left')
    ag.leftClick(*PositionConstants.NOTICE_ACCEPT_BUTTON)
    await asyncio.sleep(1)
    ag.leftClick(*PositionConstants.MAIL_INFO_BUTTON)

    login_logger.debug(f'Read Terms on: guest')


async def read_tos_on_guests(
    playonline_windows: list[WindowType], login_data: list[LoginData]
) -> None:
    for window, account in zip(playonline_windows, login_data):
        activate_window(window)
        if account.member not in VALID_MEMBER_VALS:
            waitout_image('./img/ToS.PNG', 15)
            login_logger.debug(f'Reading TOS on guest')
            await asyncio.sleep(1)
            await guest_scroll(account)
            await asyncio.sleep(2)


def img_resolution_select(path: str) -> str:
    resolution_values = {1080, 1440, 2160}

    resolution = (
        primary_monitor_res[1] if primary_monitor_res[1] in resolution_values else 1080
    )

    return path[:-4] + str(resolution) + path[-4:]


def waitout_image(
    path: list[str],
    timeout_duration: float,
    region: tuple[int, int, int, int] = PositionConstants.IMG_REGION_PLAYONLINE,
    exception_enable=True,
) -> None | tuple[int, int, int, int]:
    start = time.perf_counter()
    while time.perf_counter() - start < timeout_duration:
        location = ag.locateCenterOnScreen(path, region=region, confidence=0.8)
        if location:
            login_logger.debug(f'found image: {path}')
            return location
    else:
        if exception_enable:
            raise TimeoutException(f'Could not find Image: {path}')


def get_ffxi_windows() -> list[WindowType] | None:
    return [
        window
        for window in ag.getWindowsWithTitle('Final Fantasy XI')
        if window.title.lower() == 'final fantasy xi'
    ]


async def find_ffxi_windows(
    window_count: int, already_running_window_ids: set[int], timeout_duration: float
) -> None | list[WindowType]:
    start = time.perf_counter()
    ffxi_windows = []
    while time.perf_counter() - start < timeout_duration:
        ffxi_windows = [
            window
            for window in get_ffxi_windows()
            if window._hWnd not in already_running_window_ids
        ]

        if ffxi_windows and len(ffxi_windows) == window_count:
            return ffxi_windows
        await asyncio.sleep(0.5)
    else:
        raise TimeoutException(f'Could not find all the ffxi windows')


async def playonline_to_ffxi_window_transition(
    accounts: list[LoginData],
    playonline_windows: list[WindowType],
) -> None:
    start = time.perf_counter()
    window_count = len(playonline_windows)
    login_logger.debug(
        f'Starting transition from **{window_count}** playonline windows to ffxi windows'
    )
    while time.perf_counter() - start and len(playonline_windows) > 0:
        activate_window(playonline_windows[0])
        await asyncio.sleep(1)
        playonline_windows = find_playonline_windows(accounts, enable_exception=False)
        if window_count != len(playonline_windows):
            login_logger.debug(
                f'Currently {len(playonline_windows)} playonline windows remaining'
            )
            window_count = len(playonline_windows)

    login_logger.debug(f'Completed transition from playonline windows to ffxi windows')


async def select_ffxi_character(
    ffxi_windows: list[WindowType],
    accounts: list[LoginData],
    window_dims: list[tuple[int, int]],
) -> None:
    login_logger.debug('start ffxi window accepts')
    for window, account in zip(ffxi_windows, accounts):
        activate_window(window)
        ag.moveTo(1, 1)  # Cursor can overlap img, and thus get stuck
        accept_position = waitout_image(
            img_resolution_select('./img/AcceptDecline.PNG'),
            10,
            PositionConstants.IMG_REGION_FFXI,
        )
        login_logger.debug(f'Found accept/decline image')
        await asyncio.sleep(0.3)
        ag.leftClick(*accept_position)

    # On character select hit enter once
    for window, account in zip(ffxi_windows, accounts):
        activate_window(window)
        ag.moveTo(1, 1)
        select_position = waitout_image(
            img_resolution_select('./img/SelectCharacter.PNG'),
            10,
            PositionConstants.IMG_REGION_FFXI,
        )
        login_logger.debug(f'Found selectcharacter image')
        await asyncio.sleep(0.3)
        ag.leftClick(*select_position)

    # On second character select hit enter twice (maybe .2 seconds apart)
    for window, account, dim in zip(ffxi_windows, accounts, window_dims):
        activate_window(window)
        ag.moveTo(1, 1)
        # await asyncio.sleep(1)
        second_select_position = waitout_image(
            img_resolution_select('./img/SecondSelectCharacter.PNG'),
            10,
            PositionConstants.IMG_REGION_FFXI,
        )
        login_logger.debug(f'Found secondselectcharacter image')
        await asyncio.sleep(0.3)
        ag.leftClick(*PositionConstants.CHARACTER_SELECT_SECOND)
        await asyncio.sleep(0.3)
        ag.leftClick(*PositionConstants.CHARACTER_SELECT_THIRD)
        await asyncio.sleep(0.3)
        window.resizeTo(*dim)


def get_console_window() -> WindowType:
    console_window: WindowType = [
        window
        for window in gw.getWindowsWithTitle('LoginAssistFFXI.exe')
        if window.title.endswith('LoginAssistFFXI.exe')
    ]

    if console_window:
        console_window = console_window[0]

        console_window.moveTo(
            primary_monitor_res[0] - console_window.size[0],
            0,
        )

    return console_window


def clear_debug_log() -> None:
    with open(r'./debug.log', 'w') as f:
        pass


async def main() -> None:
    try:
        clear_debug_log()
        get_console_window()
        login_logger.debug(f'Monitor Resolution: {ag.size()}')
        all_char_data = LoginDataValidator.parse_login_data()
        windower_profiles = LoginDataValidator.gather_windower_profiles(all_char_data)
        char_names = LoginDataValidator.gather_charnames(all_char_data)

        psb = ProfileSelectBox(windower_profiles, char_names)
        accounts_to_login = psb.selected_profile

        already_running_ffxi_window_ids = set(
            [window._hWnd for window in get_ffxi_windows()]
        )

        playonline_windows = find_playonline_windows(accounts_to_login)

        await move_and_resize_windows(playonline_windows)

        await asyncio.sleep(2)

        await login_to_playonline(playonline_windows, accounts_to_login)

        await read_tos_on_guests(playonline_windows, accounts_to_login)

        await start_ffxi(playonline_windows, accounts_to_login)

        await playonline_to_ffxi_window_transition(
            accounts_to_login, playonline_windows
        )

        ffxi_windows = await find_ffxi_windows(
            len(accounts_to_login), already_running_ffxi_window_ids, 120
        )
        window_dimensions = await move_and_resize_windows(
            ffxi_windows, *PositionConstants.FFXI_RESOLUTION
        )
        await asyncio.sleep(1)
        await select_ffxi_character(ffxi_windows, accounts_to_login, window_dimensions)
    except MissingPlayonlineWindowException as e:
        login_logger.debug(
            f'Account count: {e.account_count}, Window Count {e.window_count}, need to be equal'
        )
        login_logger.exception(e)
    except Exception as e:
        login_logger.exception(e)


if __name__ == '__main__':
    asyncio.run(main())
