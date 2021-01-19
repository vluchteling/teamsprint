from __future__ import print_function

from tkinter import *

from steam.client import SteamClient
from steam.enums import EResult


class SteamClientAPI:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = None
        self.root = None
        self.twofa_entry = None
        self.email_key = None
        self.Entry = None
        self.Label = None
        self.beginscherm = None

    def open_client(self, root=None, guirequired=False, beginscherm=None, emailkey=None, twofakey=None):
        self.beginscherm = beginscherm

        self.client = SteamClient()
        self.client.set_credential_location(".")  # where to store sentry files and other stuff
        try:
            result = self.client.login(username=self.username, password=self.password, auth_code=emailkey, two_factor_code=twofakey)

            if result == EResult.OK:
                if guirequired:
                    self.beginscherm.open_GUI(self)

                return "ok"

            if result == EResult.InvalidPassword or result == EResult.InvalidName:
                return "password"
            if result == EResult.InvalidLoginAuthCode :
                self.open_keyscherm(extra_text="foute code!")
            if result == EResult.ServiceUnavailable:
                return "unavailable"

            if result == EResult.AccountLogonDenied:
                if root is not None:
                    root.destroy()
                self.open_keyscherm()
            if result == EResult.AccountLoginDeniedNeedTwoFactor:
                if root is not None:
                    root.destroy()
                self.open_keyscherm()

            else:
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

    def log_in(self):
        print("-" * 20)
        print("Logged on as:", self.client.user.name)
        print("Community profile:", self.client.steam_id.community_url)
        print("Last logon:", self.client.user.last_logon)
        print("Last logoff:", self.client.user.last_logoff)
        print("Press ^C to exit")

    def change_personastate(self, status):
        if status == "afwezig":
            self.client.change_status(persona_state=3)
        if status == "aanwezig":
            self.client.change_status(persona_state=1)

    def log_out(self):
        if self.client.connected:
            self.client.logout()

    def get_client(self):
        return self.client

    def get_credentials(self):
        return self.username, self.password

    def open_keyscherm(self, extra_text=""):
        self.root = Tk()
        self.Label = Label(text=f"{extra_text}\nVoer hier de code in: ")
        self.Entry = Entry()
        bevestigButton = Button(text="Bevestig", command=self.confirm_key)
        stopButton = Button(text="Sluit", command=self.quit)
        self.Label.pack()
        self.Entry.pack()
        bevestigButton.pack(fill=X)

        stopButton.pack(fill=X)
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

    def open_keyscherm2(self, extra_text=""):
        self.root = Tk()
        self.Label = Label(text=f"{extra_text}\nVoer hier de code in: ")
        self.Entry = Entry()
        bevestigButton = Button(text="Bevestig", command=self.confirm_key2)
        stopButton = Button(text="Sluit", command=self.quit)
        self.Label.pack()
        self.Entry.pack()
        bevestigButton.pack(fill=X)

        stopButton.pack(fill=X)
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

    def confirm_key(self):
        self.open_client(guirequired=True, beginscherm=self.beginscherm, emailkey=self.Entry.get())
        self.root.destroy()

    def confirm_key2(self):
        self.root.destroy()
        self.open_client(guirequired=True, beginscherm=self.beginscherm, twofakey=self.Entry.get())

    def message(self):
        pass

    def quit(self):
        raise SystemExit
