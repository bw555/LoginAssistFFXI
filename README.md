# Login Assist for FFXI

This is a python3 project intended to at least partially automate the tedious login process of final fantasy xi's playonline login system.

This is primarily accomplished with the PyAutoGUI library. This library can programmatically: move and resize windows, move and click your mouse, and type using your keyboard. Using this program requires leaving PyAutoGUI to do these things for minutes at a time with no input from you, with the exception of you having to enter one time passwords (if enabled). The failsafes that let you exit this loop in case things go wrong can also be quite irritating. If you are not comfortable with that I do not recommend using this program. For those interested, links to the source code and documentation of PyAutoGUI are listed below:

-   [Documentation](https://pyautogui.readthedocs.org)
-   [Source Code](https://github.com/asweigart/pyautogui)

This program also requires you to have your account information in a local json file which is used to enter in your login data. If you are not comfortable with that I do not recommend using this program.

Releases of LoginAssistFFXI can be found below:

-   [Releases page](https://github.com/bw555/LoginAssistFFXI/releases)

## Setup and running LoginAssistFFXI

1. Please note that some parts of this programs logic depend somewhat on the resolution of your monitor. This has mostly been tested on 1920x1080, and 3840x2160 monitors. I at the very least suspect people with resolutions outside of this may run into LoginAssist closing only part way through the login process, particularly after transitioning from playonline to FFXI windows. Please see the feedback section below in the event you run into problems.
2. First find the file called login_data.json under the data folder. Some examples of appropriate account values have been provided as illustration. Any accounts you want to login via the Guest Login tab should be put at the top of the member accounts with `"guest":true` being set. Any unused accounts should be removed from this file. **Please note the lack of a trailing comma after the final } in the file**.
3. **Notice that the member accounts with `"guest": false` set MUST be in the same order from top to bottom as they are in the following image**
   ![PlayonlineLoginScreen](img/PlayonlineExample.png)
4. If you only want to login one character the file should look something like this, with your actual account values substitued in and `"guest": false` being set if your single account is the top spot in the member list:

    ```
    [
         {
             "character_name":"GuestOne",
             "playonline_id":"GUES1111",
             "playonline_password":"passwordP",
             "square_enix_id":"Test123",
             "square_enix_password":"passwordSE",
             "onetimepassword_enabled": false,
             "guest":true
         }
     ]
    ```

5. If you use two factor authentication for any particular account make sure you set `"onetimepassword_enabled": true` for the accounts with it active.
6. LoginAssist is currently not able to deal with the screens where you must wait to download files after an update. Make sure FFXI is completely up to date after every monthly update before trying to use LoginAssist.
7. You must have open on your primary monitor the same amount of playonline windows as you have listed in the file. In the example login_data.json file there are six accounts, therefore you would need to have 6 playonline windows open to the screen in the image above.
8. **Before running LoginAssistFFXI you should probably know how to stop it. There are currently two failsafes to stop the program:**
    1. Place your mouse cursor into the top left corner of your primary monitor. Unfortunately, I have found this failsafe's behaviour to be quite persnickety. You may need to try several times to get this to work.
    2. You will notice a black console window that moves to the top right of your screen. If you click on the top right X, it will also stop the program. Picture below: ![LoginAssistConsole](./img/EmergencyExitConsole.png)
9. If you are using Windower, I recommend making sure the plugin WinControl/position_manager are disabled until you are fully logged in.
10. Once all of your playonline windows are on your primary monitor as well as your mouse cursor, you can run LoginAssistFFXI.exe. Keep in mind you will need to run it as an administrator.
11. If you have one time passwords active, you will still have to manually enter it for each character in the popup box shown below. Just **left click** the ok button after entering it. After all of those are entered you should (hopefully) just have to wait until you are logged in!

![TwoFactorAuthBox](./img/OneTimePasswordBox.PNG)

## Feedback

-   You should notice a file called debug.log that updates every time you run LoginAssistFFXI. If you are willing please post the contents of that file in the event you run in to trouble and post it on the [github issues page](https://github.com/bw555/LoginAssistFFXI/issues)

### Creating LoginAssistFFXI from source

-   LoginAssistFFXI.exe is created using pyinstaller with the following command:
-   `pyinstaller --noconfirm --onefile --console main.py --distpath "./" -n "LoginAssistFFXI"`

### Future Ideas

-   I would like to change the data/login_data.json file to an xml file to keep it consistent with settings files windower users may be familiar with.
-   Find a better solution for the program failsafes, perhaps via a homemade GUI.
-   Replace some of the clumsy sleep logic used in the playonline window section with the image logic in order to know when to advance.
-   Add a setting that can choose which character you want to login to from the character selection list. LoginSelect currently chooses the character in the top left of the list.
