from __future__ import print_function
from steam.client import SteamClient
from getpass import getpass
from steam.enums import EResult

print("One-off login recipe")
print("-" * 20)

LOGON_DETAILS = {
    'username': input("Steam user: "),
    'password': getpass("password please: "),
}

client = SteamClient()




@client.on('error')
def error(result):
    print("Logon result:", repr(result))



@client.on("logged_on")
def handle_after_logon():

    print("-" * 20)
    print("Logged on as:", client.user.name)
    print("Community profile:", client.steam_id.community_url)
    print("Last logon:", client.user.last_logon)
    print("Last logoff:", client.user.last_logoff)
    print("Press ^C to exit")


try:
    result = client.cli_login(**LOGON_DETAILS)

    if result != EResult.OK:
        print("Failed to login: %s" % repr(result))
        raise SystemExit

    client.run_forever()
except KeyboardInterrupt:
    if client.connected:
        print("Logout")
        client.logout()



