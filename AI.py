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

        # De GUI code
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.groot_font = Font(size=30)
        self.root.configure(bg="#2f2c2f")
        self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                    background="#5a565a", foreground="white", font=self.groot_font)
        self.gamesframe = Frame()

        #self.gameslabel = Label(font=self.groot_font, background="#5a565a")
        self.gamesframe.pack()
        games = self.haal_data_op()
        self.toon_data(games)
        self.maak_data(games)
        self.afsluitButton.pack()
        self.root.mainloop()

    def haal_data_op(self):
        steamid = 76561199119177557
        api = SteamWebAPI()
        text = api.get_steam_games_from_user(steamid)
        legelist= []

        games = text['response']['games']
        for game in games:
            legelist.append(game["name"])
        return games

    def toon_data(self, data):
        koppen = ('appid', "name", "playtime_forever (min)")
        self.treeview = Treeview(self.gamesframe, columns=koppen, show='headings', )
        scrollbar = Scrollbar(self.gamesframe)
        self.treeview.config(yscrollcommand=scrollbar.set)
        for col in koppen:
            self.treeview.heading(col, text=col)
        #friendlist = self.sorteer_data(friendlist)

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
        print(f"Gemiddelde speeltijd per game: {totaaltijd/counter}")





    def stop(self):


        """ Deze functie sluit de applicatie af. """
        if self.root is not None:
            self.root.destroy()
            self.root = None
