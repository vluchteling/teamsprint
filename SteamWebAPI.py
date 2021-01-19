import json
import urllib.request


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
        text = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.APIKEY}" \
               f"&steamid={steamid}&relationship=friend"
        with urllib.request.urlopen(text) as url:
            data = json.loads(url.read().decode())
        return data

    def friendstatus(self, steamid):
        text = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.APIKEY}' \
               f'&steamids={steamid}'
        with urllib.request.urlopen(text) as url:
            data = json.loads(url.read().decode())
        return data

    def get_news(self):
        text = f' http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300' \
               f'&format=json'
        with urllib.request.urlopen(text) as url:
            data = json.loads(url.read().decode())
        return data

    def get_procent(self, Appid):
        text = f'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/' \
               f'?gameid={Appid}&format=json'
        with urllib.request.urlopen(text) as url:
            data = json.loads(url.read().decode())
        return data
