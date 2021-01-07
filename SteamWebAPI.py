import urllib.request
import json


class SteamWebAPI:
    def __init__(self):
        self.APIKEY = "CE13AFE10AEE3CBD7F2BB6FB76338F2B"

    def get_steam_games_from_user(self, steamid):
        text = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.APIKEY}" \
               f"&steamid={steamid}&format=json&include_appinfo=true "
        with urllib.request.urlopen(text) as url:
            data = json.loads(url.read().decode())
        return data

    def get_friend_list(self, steamid):
        text = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.APIKEY}&steamid={steamid}&relationship=friend"
        with urllib.request.urlopen(text) as url:
            data = json.loads(url.read().decode())
        return data
