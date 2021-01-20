import os
from tkinter import *
from tkinter.font import Font

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

from Rekenmachine import Rekenmachine
from SteamWebAPI import SteamWebAPI


class DataScherm:
    def __init__(self, client, root, gui):
        """ de init functie van het object"""
        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi
        self.client = client
        self.api = SteamWebAPI()
        self.gui = gui
        self.root = root
        self.rekenmachine = Rekenmachine()

        self.hoofdframe = None
        self.linkerframe = None
        self.rechterframe = None
        self.buttonframe = None
        self.afsluitButton = None
        self.bar_gem_speeltijd = None
        self.bar_tot_speeltijd = None
        self.bar_aantal_games = None
        self.hist = None

        self.open_gui()
        self.haal_speeltijd_data_op()

    def open_gui(self):
        """ Deze functie laadt de gui objecten."""
        bgcolor = "#4B0082"
        groot_font = Font(size=30)
        self.hoofdframe = Frame()
        self.linkerframe = Frame(self.hoofdframe)
        self.rechterframe = Frame(self.hoofdframe)
        self.buttonframe = Frame(width=self.root.winfo_screenwidth(), height=20, background="#2f2c2f")
        self.afsluitButton = Button(self.buttonframe, text="Afsluiten", command=self.stop,
                                    background=bgcolor, foreground="white", font=groot_font)
        self.linkerframe.pack(side=LEFT, expand=1, fill=BOTH)
        self.rechterframe.pack(side=RIGHT, expand=1, fill=X)
        self.hoofdframe.pack(side=TOP, expand=1, fill=X)
        self.afsluitButton.pack()
        self.buttonframe.pack(side=BOTTOM, expand=True)

    def haal_friendlist_data_op(self):
        """ Deze functie haalt de friendlist van de gebruiker op, en maak een lijst met id nummers van de vrienden
        en een dict om ze terug te kunnen koppelen aan de naam"""
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

    def haal_speeltijd_data_op(self):
        """ Deze functie haalt de speeltijden op van de gebruiker en de vrienden, en berekent de totaaltijden,
        en geeft de opdracht om de grafieken te maken."""
        friendsdata, friendsdict = self.haal_friendlist_data_op()
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
                    if game['playtime_forever'] > 0:
                        grote_tijdslijst.append(game['playtime_forever'])
                gemtijdlist.append([friendsdict[friend], totaaltijd / counter])
                totaaltijdlist.append([friendsdict[friend], totaaltijd])
                aantalgameslist.append([friendsdict[friend], counter])

            except KeyError:
                continue
        self.maak_gem_speeltijd_grafiek(gemtijdlist)
        self.maak_tot_speeltijd_grafiek(totaaltijdlist)
        self.maak_aantal_games_grafiek(aantalgameslist)
        self.maak_histogram(grote_tijdslijst)

    def maak_gem_speeltijd_grafiek(self, data):
        """ Deze functie maakt de gemiddelde speeltijd grafiek"""
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
        dataframe.plot(kind='bar', legend=False, ax=subplot, grid=True)
        subplot.set_title('Gemiddelde speeltijd per game (in minuten).')
        self.bar_gem_speeltijd.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

    def maak_tot_speeltijd_grafiek(self, data):
        """ Deze functie maakt de totale speeltijd grafiek. """
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
        dataframe.plot(kind='bar', legend=False, ax=subplot, grid=True)
        subplot.set_title('totale speeltijd per user (in minuten).')
        self.bar_tot_speeltijd.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

    def maak_aantal_games_grafiek(self, data):
        """ Deze fucntie maakt de aantal games grafiek."""
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
        dataframe.plot(kind='bar', legend=False, ax=subplot, grid=True)
        subplot.set_title('aantal games per user.')
        self.bar_aantal_games.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

    def stop(self):
        """ Deze functie stopt het grafiekenscherm. """
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

    def maak_histogram(self, data):
        """ Deze functie maakt met behulp van het Freedman-Diaconis algoritme een soort histogram aan,
        als er te veel klassen wordt een simpeler algoritme gebruikt."""
        hoogste = 0
        laagste = None
        for tijd in data:
            if tijd > hoogste:
                hoogste = tijd
            if laagste is None or tijd < laagste:
                laagste = tijd

        interkwartielrange = self.rekenmachine.q3(data) - self.rekenmachine.q1(data)
        klassengrootte = (2 * interkwartielrange) / len(data) ** (1 / 3)
        klassenlijst = []
        vorige_x = laagste
        for x in range(int(laagste), int(hoogste) + int(klassengrootte), int(klassengrootte)):
            if x != laagste:
                klassenlijst.append([vorige_x, x])
                vorige_x = x
            else:
                vorige_x = x

        frequentiedict = {}

        for klasse in klassenlijst:
            for punt in data:
                if klasse[0] <= punt < klasse[1]:
                    frequentiedict[f"{klasse[0]}-{klasse[1]}"] = frequentiedict.get(f"{klasse[0]}-{klasse[1]}", 0) + 1

        if len(frequentiedict.keys()) <= 20:

            # hierna is het niet meer leesbaar
            dataframe = DataFrame.from_dict(frequentiedict, orient='index')
            plot = plt.Figure(figsize=(5, 3.5))
            subplot = plot.add_subplot(211)
            self.hist = FigureCanvasTkAgg(plot, self.linkerframe)
            dataframe.plot(kind='bar', legend=False, ax=subplot, xlabel="Speeltijd in minuten.", ylabel="frequentie",
                           grid=True)
            subplot.set_title(
                'Staafdiagram van de speeltijden van jou en je vrienden.\n (x-as: tijd in minuten, niet gespeelde spellen uitgesloten.)')
            self.hist.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)

        else:
            klassenbreedte = hoogste - laagste
            klassengrootte = int(klassenbreedte / 20) + 1
            klassenlijst = []
            vorige_x = laagste
            for x in range(int(laagste), int(hoogste) + int(klassengrootte), int(klassengrootte)):
                if x != laagste:
                    klassenlijst.append([vorige_x, x])
                    vorige_x = x
                else:
                    vorige_x = x

            frequentiedict = {}

            for klasse in klassenlijst:
                for punt in data:
                    if klasse[0] <= punt < klasse[1]:
                        frequentiedict[f"{klasse[0]}-{klasse[1]}"] = frequentiedict.get(f"{klasse[0]}-{klasse[1]}",
                                                                                        0) + 1
            dataframe = DataFrame.from_dict(frequentiedict, orient='index')
            plot = plt.Figure(figsize=(5, 3.5))
            subplot = plot.add_subplot(211)
            self.hist = FigureCanvasTkAgg(plot, self.linkerframe)
            dataframe.plot(kind='bar', legend=False, ax=subplot, xlabel="Speeltijd in minuten.", ylabel="frequentie",
                           grid=True)
            subplot.set_title(
                'Staafdiagram van de speeltijden van jou en je vrienden.\n (x-as: tijd in minuten, niet gespeelde spellen uitgesloten.)')
            self.hist.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, pady=1, padx=1)
