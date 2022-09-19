import tkinter as tk
from LoginData import LoginData
from CustomExceptions import InvalidProfileException
from LoginDataValidator import get_requested_accounts

DEFAULT_BUTTON_TEXT = 'No valid profile entered'


class ProfileSelectBox:
    def __init__(self, profiles: dict[str, list[LoginData]], char_names: set[str]):
        self.profiles = profiles
        self.selected_profile: None | list[LoginData] = None
        self.char_names = char_names

        self.window = tk.Tk()
        self.window.title('Profile Selection')
        self.window.option_add('*font', 'consolas 12')
        tk.Label(self.window, text='Windower Profile').grid(row=0, column=0)
        tk.Label(self.window, text='Characters').grid(row=0, column=1)
        for i, (profile, accounts) in enumerate(self.profiles.items()):
            tk.Label(self.window, text=f'{profile:>}').grid(row=i + 1, column=0)
            names = [account.char_name for account in accounts]
            tk.Label(self.window, text=f'{", ".join(names):<}').grid(
                row=i + 1, column=1
            )

        self.instruction = tk.Label(
            text='Enter profile name (or single character name):'
        )
        self.instruction.grid(row=len(self.profiles) + 1, column=0)

        self.profile_entry = tk.Entry(master=self.window)
        self.profile_entry.grid(row=len(self.profiles) + 1, column=1)
        self.profile_entry.bind('<KeyRelease>', self.check_profile_validity)

        self.confirm_button = tk.Button(
            self.window,
            text=DEFAULT_BUTTON_TEXT,
            fg='white',
            state=tk.DISABLED,
            command=self.login_selected,
        )
        self.confirm_button.grid(columnspan=2)

        self.window.mainloop()

    def check_profile_validity(self, event) -> None:
        if self.profile_entry.get() in self.profiles:
            names = [
                account.char_name
                for account in self.profiles.get(self.profile_entry.get())
            ]
            self.confirm_button['state'] = tk.NORMAL
            self.confirm_button['text'] = f'Click here to login on {", ".join(names)}'
            self.confirm_button['bg'] = 'green'
        elif self.profile_entry.get() in self.char_names:
            self.confirm_button['state'] = tk.NORMAL
            self.confirm_button[
                'text'
            ] = f'Click here to login on {self.profile_entry.get()}'
            self.confirm_button['bg'] = 'green'
        else:
            self.confirm_button['state'] = tk.DISABLED
            self.confirm_button['text'] = DEFAULT_BUTTON_TEXT
            self.confirm_button['bg'] = '#f0f0f0'

    def login_selected(self) -> str:
        self.selected_profile = get_requested_accounts(self.profile_entry.get())
        self.window.destroy()
