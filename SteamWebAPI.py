import json
import urllib.request
from urllib.error import HTTPError


class SteamWebAPI:
    def __init__(self):
        """ init fucntie van de class"""
        self.APIKEY = "CE13AFE10AEE3CBD7F2BB6FB76338F2B"

    def get_steam_games_from_user(self, steamid):
        """ Deze functie haalt de games op van een steamid"""
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
        """ deze functie haalt de friendlist van een steamid op"""
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
        """ deze functie haalt een gebruiker op"""
        try:
            text = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.APIKEY}' \
                   f'&steamids={steamid}'
            with urllib.request.urlopen(text) as url:
                data = json.loads(url.read().decode())
            return data
        except HTTPError:
            print("steam is weer eens offline!")
            raise SystemExit

    def get_procent(self, Appid):
        """ Deze functie haalt achievement percentages op van een game."""
        try:
            text = f'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/' \
                   f'?gameid={Appid}&format=json'
            with urllib.request.urlopen(text) as url:
                data = json.loads(url.read().decode())
            return data
        except HTTPError:
            print("steam is weer eens offline!")
            raise SystemExit
