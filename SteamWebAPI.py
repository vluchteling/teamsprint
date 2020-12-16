import urllib.request
import json


class SteamWebAPI:

    def get_steam_games_from_user(self, steamid):
        text = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=CE13AFE10AEE3CBD7F2BB6FB76338F2B" \
               f"&steamid={steamid}&format=json&include_appinfo=true "
        with urllib.request.urlopen(text) as url:
            data = json.loads(url.read().decode())
        return data
