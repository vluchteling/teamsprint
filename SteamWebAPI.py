import json
import urllib.request
from urllib.error import HTTPError


class SteamWebAPI:
    def __init__(self):
        self.APIKEY = "CE13AFE10AEE3CBD7F2BB6FB76338F2B"

    def get_steam_games_from_user(self, steamid):
        try:
            text = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.APIKEY}" \
                   f"&steamid={steamid}&format=json&include_appinfo=true "
            with urllib.request.urlopen(text) as url:
                data = json.loads(url.read().decode())
            return data
        except HTTPError:
            print("steam is weer eens offline!")
            raise SystemExit

    def get_friend_list(self, steamid):
        try:
            text = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.APIKEY}" \
                   f"&steamid={steamid}&relationship=friend"
            with urllib.request.urlopen(text) as url:
                data = json.loads(url.read().decode())
            return data
        except HTTPError:
            print("steam is weer eens offline!")
            raise SystemExit

    def friendstatus(self, steamid):
        try:
            text = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.APIKEY}' \
                   f'&steamids={steamid}'
            with urllib.request.urlopen(text) as url:
                data = json.loads(url.read().decode())
            return data
        except HTTPError:
            print("steam is weer eens offline!")
            raise SystemExit

    def get_news(self):
        try:
            text = f' http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300' \
                   f'&format=json'
            with urllib.request.urlopen(text) as url:
                data = json.loads(url.read().decode())
            return data
        except HTTPError:
            print("steam is weer eens offline!")
            raise SystemExit

    def get_procent(self, Appid):
        try:
            text = f'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/' \
                   f'?gameid={Appid}&format=json'
            with urllib.request.urlopen(text) as url:
                data = json.loads(url.read().decode())
            return data
        except HTTPError:
            print("steam is weer eens offline!")
            raise SystemExit
