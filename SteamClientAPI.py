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

        client = SteamClient()

        # @client.on('error')
        # def error(result):
        # print("Logon result:", repr(result))

        @client.on("logged_on")
        def handle_after_logon():
            print("-" * 20)
            print("Logged on as:", client.user.name)
            print("Community profile:", client.steam_id.community_url)
            print("Last logon:", client.user.last_logon)
            print("Last logoff:", client.user.last_logoff)
            print("Press ^C to exit")

        try:
            result = client.cli_login(**self.credentials)

            if result != EResult.OK:
                print("Failed to login: %s" % repr(result))
                raise SystemExit

            client.run_forever()
        except KeyboardInterrupt:
            if client.connected:
                print("Logout")
                client.logout()


SteamClientAPI()
