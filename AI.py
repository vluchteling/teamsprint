import os
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Treeview
from SteamWebAPI import SteamWebAPI


class DataScherm:
    def __init__(self, client):
        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi
        self.client = client
        self.api = SteamWebAPI()

        # De GUI code
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.groot_font = Font(size=30)
        self.root.configure(bg="#2f2c2f")
        self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                    background="#5a565a", foreground="white", font=self.groot_font)
        self.gamesframe = Frame()

        self.gamesframe.pack()
        friendsdata = self.haal_data_op()
        for friend in friendsdata:
            games = friendsdata[friend]['response']['games']
            self.toon_data(games)
            self.maak_data(games)

        self.afsluitButton.pack()
        self.root.mainloop()

    def haal_data_op(self):
        steamid = self.client.get_client().steam_id.as_64
        data = self.api.get_friend_list(steamid)
        friendjson = data['friendslist']['friends']
        friendlist = []
        for friend in friendjson:
            friendid = friend['steamid']
            friendlist.append(friendid)
        friendgamesdict = {}
        for friend in friendlist:
            print(self.api.get_steam_games_from_user(friend)['response']['games'])
            friendgamesdict[friend] = self.api.get_steam_games_from_user(friend)
        return friendgamesdict

    def toon_data(self, data):
        koppen = ('appid', "name", "playtime_forever (min)")
        self.treeview = Treeview(self.gamesframe, columns=koppen, show='headings', )
        scrollbar = Scrollbar(self.gamesframe)
        self.treeview.config(yscrollcommand=scrollbar.set)
        for col in koppen:
            self.treeview.heading(col, text=col)

        for game in data:
            print(game)
            self.treeview.insert("", "end",
                                 values=(game['appid'], game['name'], game['playtime_forever']))

        self.treeview.pack()
        scrollbar.config(command=self.treeview.yview)

    def maak_data(self, data):
        counter = 0
        totaaltijd = 0
        for game in data:
            counter += 1
            totaaltijd += game['playtime_forever']
        print(f"Gemiddelde speeltijd per game: {totaaltijd / counter}")

    def stop(self):
        self.root.destroy()

        """ Deze functie sluit de applicatie af. """
        if self.root is not None:
            self.root = None

    def achievements(self):
        data = self.api.get_friend_list(steamid=self.client.get_client().steam_id.as_64)
        friendjson = data['friendslist']['friends']
        friend = friendjson[0]['steamid']
        gameslst = self.api.get_steam_games_from_user(friend)
        appid = gameslst['response']['games'][0]['appid']
        data2 = self.api.get_procent(Appid=appid)

        percentages = data2['achievementpercentages']['achievements']

        leeglst = []
        for percentage in percentages:
            leeglst.append(percentage['percent'])
        print(self.sorteer_data(leeglst))

    def sorteer_data(self, data):
        self.quicksort(data, 0, len(data) - 1)
        """ Deze funtie sorteert de ingevoerde data."""
        return data

    def partition(self, arr, min, max):
        kleinste = (min - 1)
        grootste = arr[max]

        for j in range(min, max):

            if arr[j] < grootste:
                kleinste = kleinste + 1
                arr[kleinste], arr[j] = arr[j], arr[kleinste]

        arr[kleinste + 1], arr[max] = arr[max], arr[kleinste + 1]
        return kleinste + 1

    def quicksort(self, lst, min, max):
        if min < max:
            pi = self.partition(lst, min, max)
            self.quicksort(lst, min, pi - 1)
            self.quicksort(lst, pi + 1, max)
