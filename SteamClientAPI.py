from __future__ import print_function
from steam.client import SteamClient
from getpass import getpass
from steam.enums import EResult


class SteamClientAPI:

    def __init__(self):
        self.credentials = {
            'username': input("Steam user: "),
            'password': getpass("Password: "),
            # VERGEET IN CONFIGURATION "emulate terminal in output console" aan te doen!
        }

        self.client = SteamClient()

        @self.client.on('error')
        def error(result):

            if result != EResult.AccountLogonDenied:
                print("Logon result:", repr(result))

        @self.client.on('logged_on')
        def handle_after_logon():
            self.log_in()

        try:
            result = self.client.cli_login(**self.credentials)

            if result != EResult.OK:
                print("Failed to login: %s" % repr(result))
                raise SystemExit

            self.client.run_forever()
        except KeyboardInterrupt:
            if self.client.connected:
                print("Logout")
                self.client.logout()

    def log_in(self):
        print("-" * 20)
        print("Logged on as:", self.client.user.name)
        print("Community profile:", self.client.steam_id.community_url)
        print("Last logon:", self.client.user.last_logon)
        print("Last logoff:", self.client.user.last_logoff)
        print("Press ^C to exit")


SteamClientAPI()
