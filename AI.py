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
        # De GUI code
        self.root = root
        self.groot_font = Font(size=30)
        self.hoofdframe = Frame()
        self.linkerframe = Frame(self.hoofdframe)
        self.rechterframe = Frame(self.hoofdframe)
        self.buttonframe = Frame(width=self.root.winfo_screenwidth(), height=20, background="#2f2c2f")
        self.afsluitButton = Button(self.buttonframe, text="Afsluiten", command=self.stop,
                                    background="#5a565a", foreground="white", font=self.groot_font)
        self.linkerframe.pack(side=LEFT, expand=1, fill=BOTH)
        self.rechterframe.pack(side=RIGHT, expand=1, fill=X)
        self.hoofdframe.pack(side=TOP, expand=1, fill=X)
        self.afsluitButton.pack()
        self.buttonframe.pack(side=BOTTOM, expand=True)
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

            except KeyError:
                continue
        self.maak_gem_speeltijd_data(gemtijdlist)
        self.maak_tot_speeltijd_data(totaaltijdlist)
        self.maak_data_aantal_games(aantalgameslist)
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

    def maak_gem_speeltijd_data(self, data):
        namenlijst = []
        tijdlijst = []
        for friend in data:
            namenlijst.append(friend[0])
            tijdlijst.append(friend[1])
        datadict = {'usernames': namenlijst,
                    'speeltijd': tijdlijst
                    }
        dataframe = DataFrame(datadict, columns=['usernames', 'speeltijd'])
        plot = plt.Figure(figsize=(5, 3.5))
        subplot = plot.add_subplot(211)
        self.bar_gem_speeltijd = FigureCanvasTkAgg(plot, self.linkerframe)
        dataframe = dataframe[['usernames', 'speeltijd']].groupby('usernames', sort=False).sum()
        dataframe.plot(kind='bar', legend=False, ax=subplot)
        subplot.set_title('Gemiddelde speeltijd per game (in minuten).')
        self.bar_gem_speeltijd.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

    def maak_tot_speeltijd_data(self, data):
        namenlijst = []
        tijdlijst = []
        for friend in data:
            namenlijst.append(friend[0])
            tijdlijst.append(friend[1])
        datadict = {'usernames': namenlijst,
                    'speeltijd': tijdlijst
                    }
        dataframe = DataFrame(datadict, columns=['usernames', 'speeltijd'])
        plot = plt.Figure(figsize=(5, 3.5))
        subplot = plot.add_subplot(211)
        self.bar_tot_speeltijd = FigureCanvasTkAgg(plot, self.rechterframe)
        dataframe = dataframe[['usernames', 'speeltijd']].groupby('usernames', sort=False).sum()
        dataframe.plot(kind='bar', legend=False, ax=subplot)
        subplot.set_title('totale speeltijd per user (in minuten).')
        self.bar_tot_speeltijd.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

    def maak_data_aantal_games(self, data):
        namenlijst = []
        tijdlijst = []
        for friend in data:
            namenlijst.append(friend[0])
            tijdlijst.append(friend[1])
        datadict = {'usernames': namenlijst,
                    'aantal games': tijdlijst
                    }
        dataframe = DataFrame(datadict, columns=['usernames', 'aantal games'])
        plot = plt.Figure(figsize=(5, 3.5))
        subplot = plot.add_subplot(211)
        self.bar_aantal_games = FigureCanvasTkAgg(plot, self.rechterframe)
        dataframe = dataframe[['usernames', 'aantal games']].groupby('usernames', sort=False).sum()
        dataframe.plot(kind='bar', legend=False, ax=subplot)
        subplot.set_title('aantal games per user.')
        self.bar_aantal_games.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

    def stop(self):
        self.linkerframe.forget()
        self.rechterframe.forget()
        self.hoofdframe.forget()
        self.afsluitButton.forget()
        self.buttonframe.forget()
        self.bar_gem_speeltijd.get_tk_widget().forget()
        self.bar_tot_speeltijd.get_tk_widget().forget()
        self.bar_aantal_games.get_tk_widget().forget()
        self.hist.get_tk_widget().forget()
        self.gui.open_gui(True)
        self.gui.start_sensoren(True)

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
        klassengrootte = int(totale_breedte / 6 + 1)
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
        for klasse in klassenlijst:
            frequentielijst.append(0)
        for klasse in klassenlijst:
            for punt in data:
                if klasse[0] <= punt < klasse[1]:
                    frequentielijst[counter] += 1
            counter += 1
        nieuwe_klassenlijst = []
        for klasse in klassenlijst:
            nieuwe_klassenlijst.append(f"{klasse[0]}-{klasse[1]}")
            counter = 0

        data1 = {'klassen': nieuwe_klassenlijst,
                 'frequenties': frequentielijst
                 }

        dataframe = DataFrame(data)
        dataframe.hist()
        plot = plt.Figure(figsize=(5, 3.5))

        subplot = plot.add_subplot(111)
        self.hist = FigureCanvasTkAgg(plot, self.linkerframe)
        dataframe.plot(kind='hist', legend=False, ax=subplot, xlabel="Speeltijd in minuten.")
        subplot.set_title('Histogram van de speeltijden van jou en je vrienden.\n (x-as: tijd in minuten)')
        self.hist.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

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
