from __future__ import print_function
from steam.client import SteamClient
from getpass import getpass
from steam.enums import EResult
from steam.enums import EPersonaState



class SteamClientAPI:

    def __init__(self):
        """self.credentials = {
            'username': input("Steam user: "),
            'password': getpass("Password: "),
            # VERGEET IN CONFIGURATION "emulate terminal in output console" NIET AAN TE DOEN!
        }"""
        self.credentials = {
            #voer hier de inloggegevens in
            # VERGEET IN CONFIGURATION "emulate terminal in output console" NIET AAN TE DOEN!
        }
        self.client = SteamClient()
        self.client.set_credential_location(".")  # where to store sentry files and other stuff
        try:
            result = self.client.cli_login(**self.credentials)

            if result != EResult.OK:
                print("Failed to login: %s" % repr(result))
                raise SystemExit



        except KeyboardInterrupt:
            if self.client.connected:
                print("Logout")
                self.client.logout()

        @self.client.on('error')
        def error(result):
            # print("Logon result:", repr(result))
            pass

        @self.client.on("channel_secured")
        def send_login():
            if self.client.relogin_available:
                self.client.relogin()

        """"@self.client.on('logged_on')
        def handle_after_logon():"""




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
        self.client.logout()
        return



