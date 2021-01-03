from __future__ import print_function
from steam.client import SteamClient
from tkinter import *
from tkinter.font import Font
from steam.enums import EResult
from steam.enums import EPersonaState


class SteamClientAPI:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = None
        self.root = None
        self.twofa_entry = None
        self.email_entry = None

    def open_client(self):

        self.client = SteamClient()
        self.client.set_credential_location(".")  # where to store sentry files and other stuff
        try:
            result = self.client.login(username=self.username, password=self.password)
            print(result)

            if result != EResult.OK:
                print("Failed to login: %s" % repr(result))
                raise SystemExit



        except KeyboardInterrupt:
            if self.client.connected:
                print("Logout")
                self.client.logout()

        @self.client.on('error')
        def error(result):
            print("Logon result:", repr(result))

        @self.client.on("channel_secured")
        def send_login():
            if self.client.relogin_available:
                self.client.relogin()

        @self.client.on(SteamClient.EVENT_AUTH_CODE_REQUIRED)
        def auth_code_prompt(is_2fa, code_mismatch):
            groot_font = Font(size=30)
            self.root = Tk()
            self.root.attributes("-fullscreen", True)
            self.groot_font = Font(size=30)
            self.root.configure(bg="#2f2c2f")
            if is_2fa:

                twofa_label = Label(font=groot_font, background="#5a565a", text="Voer 2fa code in:")
                self.twofa_entry = Entry(width=35)
                self.bevestigButton = Button(text="Bevestig", command=self.bevestig_2fa_code,
                                             background="#5a565a", foreground="white", font=groot_font)
                twofa_label.pack()
                self.twofa_entry.pack()
                self.bevestigButton.pack()

            else:
                email_label = Label(font=groot_font, background="#5a565a", text="Voer email code in:")
                self.email_entry = Entry(width=35)
                self.bevestigButton = Button(text="Bevestig", command=self.bevestig_email_code,
                                             background="#5a565a", foreground="white", font=groot_font)
                email_label.pack()
                self.email_entry.pack()
                self.bevestigButton.pack()
            self.root.mainloop()

        @self.client.on('logged_on')
        def handle_after_logon():
            self.log_in()
            print("kaas")

    def bevestig_2fa_code(self):

        code = self.twofa_entry.get()
        self.root.destroy()
        self.client.login(username=self.username, password=self.password, two_factor_code=code)

    def bevestig_email_code(self):
        code = self.email_entry.get()
        self.root.destroy()
        self.client.login(username=self.username, password=self.password, auth_code=code)

    def log_in(self):
        print("-" * 20)
        print("Logged on as:", self.client.user.name)
        print("Community profile:", self.client.steam_id.community_url)
        print("Last logon:", self.client.user.last_logon)
        print("Last logoff:", self.client.user.last_logoff)
        print("Press ^C to exit")

    def change_status(self, status):
        self.client.change_status(persona_state=status)

    def log_out(self):
        if self.client.connected:
            self.client.logout()

    def get_client(self):
        return self.client

    def get_credentials(self):
        return self.username, self.password
