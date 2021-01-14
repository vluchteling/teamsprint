import os
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Treeview

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

from SteamWebAPI import SteamWebAPI


class DataScherm:
    def __init__(self, client, root, gui):
        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi
        self.client = client
        self.api = SteamWebAPI()
        self.gui = gui
        self.treeview = None

        # De GUI code
        self.root = root
        self.groot_font = Font(size=30)
        self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                    background="#5a565a", foreground="white", font=self.groot_font)
        self.gamesframe = Frame()

        self.gamesframe.pack()
        friendsdata, friendsdict = self.haal_data_op()

        speeltijdlist = []
        for friend in friendsdata:

            try:
                games = friendsdata[friend]['response']['games']
                counter = 0
                totaaltijd = 0
                for game in games:
                    counter += 1
                    totaaltijd += game['playtime_forever']

                speeltijdlist.append([friendsdict[friend], totaaltijd/counter])
                # self.toon_data(games)

            except KeyError:
                continue
        self.maak_data(speeltijdlist)

        self.afsluitButton.pack(side=BOTTOM)

    def haal_data_op(self):
        steamid = self.client.get_client().steam_id.as_64
        data = self.api.get_friend_list(steamid)
        friendjson = data['friendslist']['friends']
        friendlist = []
        frienddict= {}
        steamid = self.client.get_client().steam_id.as_64
        gebruiker = self.api.friendstatus(steamid)
        username = gebruiker['response']['players'][0]['personaname']
        friendlist.append(steamid)
        frienddict[steamid] = username
        for friend in friendjson:
            friendid = friend['steamid']
            games = self.api.friendstatus(friend['steamid'])
            naam = games['response']['players'][0]['personaname']
            frienddict[friend['steamid']] = naam
            friendlist.append(friendid)
        friendgamesdict = {}
        for friend in friendlist:
            friendgamesdict[friend] = self.api.get_steam_games_from_user(friend)
        return friendgamesdict, frienddict

    def toon_data(self, data):
        koppen = ('appid', "name", "playtime_forever (min)")
        self.treeview = Treeview(self.gamesframe, columns=koppen, show='headings', )
        scrollbar = Scrollbar(self.gamesframe)
        self.treeview.config(yscrollcommand=scrollbar.set)
        for col in koppen:
            self.treeview.heading(col, text=col)

        for game in data:
            self.treeview.insert("", "end",
                                 values=(game['appid'], game['name'], game['playtime_forever']))

        self.treeview.pack()
        scrollbar.config(command=self.treeview.yview)

    def maak_data(self, data):
        # data = self.sorteer_data(data)

        namenlijst = []
        tijdlijst = []
        for friend in data:
            namenlijst.append(friend[0])
            tijdlijst.append(friend[1])
        data1 = {'usernames': namenlijst,
                 'gemiddelde speeltijd (in min)': tijdlijst
                 }
        df1 = DataFrame(data1, columns=['usernames', 'gemiddelde speeltijd (in min)'])
        figure1 = plt.Figure(figsize=(6, 5), dpi=75)
        ax1 = figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(figure1, self.root)
        self.bar1.get_tk_widget().pack(side=LEFT)
        df1 = df1[['usernames', 'gemiddelde speeltijd (in min)']].groupby('usernames').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Gemiddelde speeltijd per game.')


    def stop(self):
        self.gamesframe.forget()
        self.afsluitButton.forget()
        if self.treeview is not None:
            self.treeview.forget()
        self.gui.open_gui(True)
        self.gui.start_sensoren(True)
        self.bar1.get_tk_widget().forget()

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
