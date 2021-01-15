import os
from tkinter import *
from tkinter.font import Font

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

        tabelframe = Frame(width=self.root.winfo_screenwidth() / 2)
        rechterframe = Frame(width=self.root.winfo_screenwidth() / 2)
        buttonframe = Frame()
        self.afsluitButton = Button(buttonframe, text="Afsluiten", command=self.stop,
                                    background="#5a565a", foreground="white", font=self.groot_font, width=300)
        self.nwframe = Frame(tabelframe, width=self.root.winfo_screenwidth() / 2,
                             height=(self.root.winfo_screenheight() - 200 / 2))
        self.neframe = Frame(rechterframe, width=self.root.winfo_screenwidth() / 2,
                             height=(self.root.winfo_screenheight() - 200 / 2))
        self.swframe = Frame(tabelframe, width=self.root.winfo_screenwidth() / 2,
                             height=(self.root.winfo_screenheight() - 200 / 2))
        self.seframe = Frame(rechterframe, width=self.root.winfo_screenwidth() / 2,
                             height=(self.root.winfo_screenheight() - 200 / 2))
        tabelframe.pack(side=LEFT)
        rechterframe.pack(side=RIGHT)

        self.afsluitButton.pack()
        self.nwframe.pack(side=TOP)
        self.neframe.pack(side=TOP)
        self.swframe.pack(side=BOTTOM)
        self.seframe.pack(side=BOTTOM)
        buttonframe.pack(side=BOTTOM)
        friendsdata, friendsdict = self.haal_data_op()

        gemtijdlist = []
        totaaltijdlist = []
        aantalgameslist = []
        grote_tijdslijst = []

        for friend in friendsdata:

            try:
                games = friendsdata[friend]['response']['games']
                counter = 0
                totaaltijd = 0
                for game in games:
                    counter += 1
                    totaaltijd += game['playtime_forever']

                    grote_tijdslijst.append(game['playtime_forever'])

                gemtijdlist.append([friendsdict[friend], totaaltijd / counter])
                totaaltijdlist.append([friendsdict[friend], totaaltijd])
                aantalgameslist.append([friendsdict[friend], counter])
                # self.toon_data(games)

            except KeyError:
                continue
        self.maak_data(gemtijdlist)
        self.maak_data2(totaaltijdlist)
        self.maak_data3(aantalgameslist)
        self.maak_histogram(grote_tijdslijst)

    def haal_data_op(self):
        steamid = self.client.get_client().steam_id.as_64
        data = self.api.get_friend_list(steamid)
        friendjson = data['friendslist']['friends']
        friendlist = []
        frienddict = {}
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
        pass
        """koppen = ('appid', "name", "playtime_forever (min)")
        self.treeview = Treeview(self.gamesframe, columns=koppen, show='headings', )
        scrollbar = Scrollbar(self.gamesframe)
        self.treeview.config(yscrollcommand=scrollbar.set)
        for col in koppen:
            self.treeview.heading(col, text=col)

        for game in data:
            self.treeview.insert("", "end",
                                 values=(game['appid'], game['name'], game['playtime_forever']))

        self.treeview.pack()
        scrollbar.config(command=self.treeview.yview)"""

    def maak_data(self, data):
        namenlijst = []
        tijdlijst = []
        for friend in data:
            namenlijst.append(friend[0])
            tijdlijst.append(friend[1])
        data1 = {'usernames': namenlijst,
                 'speeltijd': tijdlijst
                 }
        df1 = DataFrame(data1, columns=['usernames', 'speeltijd'])
        figure1 = plt.Figure(figsize=(5, 3), dpi=100)
        ax1 = figure1.add_subplot(211)
        self.bar1 = FigureCanvasTkAgg(figure1, self.nwframe)
        self.bar1.get_tk_widget().pack()
        df1 = df1[['usernames', 'speeltijd']].groupby('usernames', sort=False).sum()
        df1.plot(kind='bar', legend=False, ax=ax1)
        ax1.set_title('Gemiddelde speeltijd per game (in minuten).')

    def maak_data2(self, data):
        namenlijst = []
        tijdlijst = []

        for friend in data:
            namenlijst.append(friend[0])
            tijdlijst.append(friend[1])
        data1 = {'usernames': namenlijst,
                 'speeltijd': tijdlijst
                 }
        df1 = DataFrame(data1, columns=['usernames', 'speeltijd'])
        figure1 = plt.Figure(figsize=(5, 3), dpi=100)
        ax1 = figure1.add_subplot(211)
        self.bar1 = FigureCanvasTkAgg(figure1, self.neframe)
        self.bar1.get_tk_widget().pack()
        df1 = df1[['usernames', 'speeltijd']].groupby('usernames', sort=False).sum()
        df1.plot(kind='bar', legend=False, ax=ax1)
        ax1.set_title('totale speeltijd per user (in minuten).')

    def maak_data3(self, data):
        namenlijst = []
        tijdlijst = []
        for friend in data:
            namenlijst.append(friend[0])
            tijdlijst.append(friend[1])
        data1 = {'usernames': namenlijst,
                 'totale speeltijd (in min)': tijdlijst
                 }
        df1 = DataFrame(data1, columns=['usernames', 'totale speeltijd (in min)'])
        figure1 = plt.Figure(figsize=(5, 3), dpi=100)
        ax1 = figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(figure1, self.seframe)
        self.bar1.get_tk_widget().pack()
        df1 = df1[['usernames', 'totale speeltijd (in min)']].groupby('usernames', sort=False).sum()
        df1.plot(kind='bar', legend=False, ax=ax1)
        ax1.set_title('aantal games per user.')

    def stop(self):
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

    def maak_histogram(self, data):
        print(data)
        tijdendata = data
        hoogste = 0
        laagste = None
        counter = 0
        for tijd in data:
            counter += 1
            if tijd > hoogste:
                hoogste = tijd
            if laagste is None or tijd < laagste:
                laagste = tijd
        totale_breedte = hoogste - laagste
        # interkwartielrange = self.q3(data) - self.q1(data)
        N = len(data)
        klassengrootte = int(totale_breedte / 6 + 1)
        # klassengrootte = int((2 *( interkwartielrange / N ** (1 / 3)) + 1))
        print(f"laagste: {laagste}, hoogste: {hoogste}")
        klassenlijst = []
        vorige_x = laagste
        for x in range(int(laagste), int(hoogste) + klassengrootte, klassengrootte):
            if x != laagste:
                klassenlijst.append([vorige_x, x])
                vorige_x = x
            else:
                vorige_x = x
        frequentielijst = []
        counter = 0
        print(data)
        for klasse in klassenlijst:
            frequentielijst.append(0)
        for klasse in klassenlijst:
            for punt in data:
                if klasse[0] <= punt < klasse[1]:
                    frequentielijst[counter] += 1
            counter += 1
        print(frequentielijst)
        nieuwe_klassenlijst = []
        for klasse in klassenlijst:
            nieuwe_klassenlijst.append(f"{klasse[0]}-{klasse[1]}")
            counter = 0

        data1 = {'klassen': nieuwe_klassenlijst,
                 'frequenties': frequentielijst
                 }

        df1 = DataFrame(data)
        df1.hist()
        print(tijdendata)
        figure1 = plt.Figure(figsize=(5, 3), dpi=100)
        ax1 = figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(figure1, self.swframe)
        self.bar1.get_tk_widget().pack()
        # df1 = df1[['frequenties']].groupby('frequenties', sort=False).sum()

        df1.plot(kind='hist', legend=False, ax=ax1)
        ax1.set_title('Histogram van de speeltijden van jou en je vrienden.')

    def median(self, lst):
        """ Retourneer de mediaan (float) van de lijst lst. """
        lst = sorted(lst)
        if len(lst) % 2 == 1:
            middelste = len(lst) / 2
            mediaan = float(lst[int(middelste)])
        else:
            pos1 = int((len(lst) - 1) // 2)
            pos2 = pos1 + 1
            middelste1 = lst[pos1]
            middelste2 = lst[pos2]
            mediaan = float(self.mean([middelste1, middelste2]))

        return mediaan

    def mean(self, lst):
        """ Retourneer het gemiddelde (float) van de lijst lst. """
        totaal = 0
        aantal = 0
        for getal in lst:
            totaal += getal
            aantal += 1
        return totaal / aantal

    def q1(self, lst):
        """
        Retourneer het eerste kwartiel Q1 (float) van de lijst lst.
        Tip: maak gebruik van median()
        """
        lst = sorted(lst)
        med = self.median(lst)
        sublijst = []
        for x in range(0, len(lst)):
            if lst[x] < med:
                sublijst.append(lst[x])
            if lst[x] == med and lst[x + 1] == lst[x]:
                sublijst.append(lst[x])
        return self.median(sublijst)

    def q3(self, lst):
        """ Retourneer het derde kwartiel Q3 (float) van de lijst lst. """
        lst = sorted(lst)
        med = self.median(lst)
        sublijst = []
        for x in range(len(lst) - 1, 0, -1):
            if lst[x] > med:
                sublijst.append(lst[x])
            if lst[x] == med and lst[x - 1] == lst[x]:
                sublijst.append(lst[x])
        return self.median(sublijst)
