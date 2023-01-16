import tkinter as tk
from tkinter import ttk
from LoginData import LoginData
from CustomExceptions import InvalidProfileException
from LoginDataValidator import get_requested_accounts

DEFAULT_BUTTON_TEXT = 'No profile or character selected.'


class ProfileSelectBox:
    def __init__(self, profiles: dict[str, list[LoginData]], char_names: set[str]):
        self.profiles = profiles
        self.selected_profile: None | list[LoginData] = None
        self.char_names = char_names
        self.selection = ''
        name_counts = [len(x) for x in profiles.values()]
        max_count = max(name_counts)

        self.window = tk.Tk()
        self.window.title('Profile/Character Selection')
        self.window.option_add('*font', 'consolas 12 bold')
        self.window.configure(bg='black')
        tk.Label(
            self.window,
            text='Windower Profile',
            background='#016001',
            foreground='white',
        ).grid(row=0, column=0, ipadx=10, padx=30, ipady=10, pady=5)
        tk.Label(
            self.window, text='Characters', background='#016001', foreground='white'
        ).grid(row=0, column=1, columnspan=max_count, ipadx=50, ipady=10, pady=5)
        for i, (profile, accounts) in enumerate(self.profiles.items()):
            tk.Button(
                self.window,
                text=f'{profile:>}'.capitalize(),
                command=lambda profile=profile: self.check_profile_validity_button(
                    profile
                ),
                background='#005C99',
                cursor='hand2',
                foreground='white',
                borderwidth=5,
            ).grid(row=i + 1, column=0, padx=20)
            names = [account.character_name for account in accounts]
            name_buttons = ttk.Frame(self.window).grid(
                row=i + 1, column=1, columnspan=max_count
            )
            for col, name in enumerate(names):
                button = tk.Button(
                    name_buttons,
                    text=f'{name.capitalize()}',
                    command=lambda name=name: self.check_profile_validity_button(name),
                    background='#005C99',
                    cursor='hand2',
                    foreground='white',
                    borderwidth=5,
                ).grid(row=i + 1, column=col + 1, columnspan=1, pady=7)

        self.confirm_button = tk.Button(
            self.window,
            text=DEFAULT_BUTTON_TEXT,
            fg='white',
            state=tk.DISABLED,
            command=self.login_selected,
            borderwidth=5,
        )
        self.confirm_button.grid(columnspan=max_count + 1, padx=10, pady=10)

        self.window.mainloop()

    def check_profile_validity_button(self, name) -> None:
        if name.lower() in {profile.lower() for profile in self.profiles}:
            names = [account.character_name for account in self.profiles.get(name)]
            self.confirm_button['state'] = tk.NORMAL
            self.confirm_button['text'] = f'Click here to login on {", ".join(names)}'
            self.confirm_button['cursor'] = 'hand2'
            self.confirm_button['bg'] = '#016001'
            self.selection = name
        elif name.lower() in {name.lower() for name in self.char_names}:
            self.confirm_button['state'] = tk.NORMAL
            self.confirm_button['text'] = f'Click here to login on {name.capitalize()}'
            self.confirm_button['cursor'] = 'hand2'
            self.confirm_button['bg'] = '#016001'
            self.selection = name
        else:
            self.confirm_button['state'] = tk.DISABLED
            self.confirm_button['text'] = DEFAULT_BUTTON_TEXT
            self.confirm_button['bg'] = '#f0f0f0'
            self.confirm_button['cursor'] = 'none'
            self.selection = ''

    def login_selected(self) -> str:
        self.selected_profile = get_requested_accounts(self.selection)
        self.window.destroy()
