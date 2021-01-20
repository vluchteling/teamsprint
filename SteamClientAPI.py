#from __future__ import print_function

from tkinter import *

from steam.client import SteamClient
from steam.enums import EResult


class SteamClientAPI:

    def __init__(self, username, password):
        """ init fucntie van de class"""
        self.username = username
        self.password = password
        self.client = None
        self.root = None
        self.twofa_entry = None
        self.email_key = None
        self.Entry = None
        self.Label = None
        self.beginscherm = None

    def open_client(self, root=None, guirequired=False, beginscherm=None):
        """Deze functie wordt aangeroepen om bij de client in te loggen werkt alleen icm beginscherm."""
        self.beginscherm = beginscherm

        self.client = SteamClient()
        self.client.set_credential_location(".")  # where to store sentry files and other stuff
        try:
            result = self.client.login(username=self.username, password=self.password, auth_code=self.email_key)

            if result == EResult.OK:
                if guirequired:
                    self.beginscherm.open_GUI(self)

                return "ok"

            if result == EResult.InvalidPassword or result == EResult.InvalidName:
                return "password"
            if result == EResult.InvalidLoginAuthCode:
                self.open_keyscherm(extra_text="foute code!")
            if result == EResult.ServiceUnavailable:
                return "unavailable"

            if result == EResult.AccountLogonDenied:
                if root is not None:
                    root.destroy()
                self.open_keyscherm()
            if result == EResult.AccountLoginDeniedNeedTwoFactor:
                print("2fa codes helaas niet gesupport, sorry.")
                raise SystemExit

            else:
                print("Failed to login: %s" % repr(result))
                raise SystemExit

        except KeyboardInterrupt:
            if self.client.connected:
                print("Logout")
                self.client.logout()

        @self.client.on('error')
        def error(result):
            """ print eventuele errors"""

            print("Logon result:", repr(result))

        @self.client.on("channel_secured")
        def send_login():
            """ Kijkt of er opnieuw ingelogd kan worden."""
            if self.client.relogin_available:
                self.client.relogin()


    def change_personastate(self, status):
        """ Verandert de status van de actieve steam client"""
        if status == "afwezig":
            self.client.change_status(persona_state=3)
        if status == "aanwezig":
            self.client.change_status(persona_state=1)

    def log_out(self):
        """ Log de actieve steam client uit."""
        if self.client.connected:
            self.client.logout()

    def get_client(self):
        """ returnt het client object"""
        return self.client

    def get_credentials(self):
        """ returnt de inloggegevens"""
        return self.username, self.password

    def open_keyscherm(self, extra_text=""):
        """ Opent het scherm om de email code op te vragen."""
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

    def confirm_key(self):
        """ logt de gebruiker in als er op de knop is gedrukt"""
        self.email_key = self.Entry.get()
        self.root.destroy()
        self.open_client(guirequired=True, beginscherm=self.beginscherm)


    def quit(self):
        """ Sluit het programma af als er op de aflsuitknop is gedrukt."""
        raise SystemExit
