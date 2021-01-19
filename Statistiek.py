from tkinter import *
from tkinter.font import Font

from Quicksort import Quicksort
from Rekenmachine import Rekenmachine
from SteamWebAPI import SteamWebAPI


class Statistiek:
    def __init__(self, client, root, gui):
        self.client = client
        self.root = root
        self.gui = gui
        self.rekenmachine = Rekenmachine()
        self.klein_font = Font(size=20)
        self.groot_font = Font(size=30)
        self.dataframe = Frame()
        scrollbar = Scrollbar(root)
        bgcolor = "#4B0082"
        self.text = Text(root, font=self.klein_font, wrap=WORD,
                         yscrollcommand=scrollbar.set, background="#411D4A", foreground="white", bd=0)
        self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                    background=bgcolor, foreground="white", font=self.groot_font)
        self.afsluitButton.pack(side=BOTTOM, pady=5)
        self.text.pack(side=TOP, expand=1, fill=BOTH)
        scrollbar.config(command=self.text.yview)
        self.webapi = SteamWebAPI()
        self.start_statistiek()

    def stop(self):
        self.afsluitButton.forget()
        self.text.forget()
        self.gui.open_gui(True)
        self.gui.start_sensoren(True)

    def start_statistiek(self):
        username = self.client.get_client().user.name
        if username is None:
            username = "onbekend"

        text = f"Hallo, {username}.\n\n"
        data = self.webapi.get_friend_list(self.client.get_client().steam_id.as_64)
        counter = 0
        friendjson = None
        try:
            friendjson = data['friendslist']['friends']
            for friend in friendjson:
                counter += 1
        except KeyError:
            pass

        text += f"Je hebt {counter} vrienden. "
        if counter < 5:
            text += "Je kan vrienden zoeken in de community tab van steam!"
        text += "\n"

        useridlist = [self.client.get_client().steam_id.as_64]
        usernamedict = {}
        if friendjson is not None:
            for friend in friendjson:
                data = (self.webapi.friendstatus(friend['steamid']))
                friendname = data["response"]["players"][0]["personaname"]
                friendid = int(friend['steamid'])
                useridlist.append(friendid)
                usernamedict[friendid] = friendname

        gamenamedict = {}
        gametimedict = {}
        gamesjson = None
        hoogste_game_aantal = 0
        hoogste_game_user = "geen"
        hoogste_speeltijd = 0
        hoogste_speeltijd_user = "geen"
        hoogste_speeltijd_appid = 0
        for user in useridlist:
            gamesdata = self.webapi.get_steam_games_from_user(user)
            try:
                gamesjson = gamesdata["response"]["games"]
                if gamesdata["response"]["game_count"] > hoogste_game_aantal:
                    hoogste_game_aantal = gamesdata["response"]["game_count"]
                    hoogste_game_user = usernamedict[user]
                for game in gamesjson:
                    if game["playtime_forever"] > hoogste_speeltijd:
                        hoogste_speeltijd = game["playtime_forever"]
                        hoogste_speeltijd_user = usernamedict[user]
                        hoogste_speeltijd_appid = game["appid"]

            except KeyError:
                pass
            if gamesjson is not None:
                for game in gamesjson:
                    gametimedict[game["appid"]] = gametimedict.get(game["appid"], 0) + game["playtime_forever"]
                    gamenamedict[game["appid"]] = game["name"]
            else:
                pass
        meest_gespeeld_appid = None
        hoogste_tijd = 0
        for game in gametimedict:
            if gametimedict[game] > hoogste_tijd:
                meest_gespeeld_appid = game
                hoogste_tijd = gametimedict[game]
        text += f"Het meest gespeelde spel is {gamenamedict[meest_gespeeld_appid]}. " \
                f"Dit is {int(hoogste_tijd / 60 / 24)} dagen gespeeld!\n"
        values = gametimedict.values()
        tijdenlist = []
        for item in values:
            tijdenlist.append(item)
        eerste_kwartiel = self.rekenmachine.q1(tijdenlist)
        derde_kwartiel = self.rekenmachine.q3(tijdenlist)
        toplijst = []
        floplijst = []
        for game in gametimedict:
            if gametimedict[game] < eerste_kwartiel:
                floplijst.append([gametimedict[game], gamenamedict[game]])
            elif gametimedict[game] > derde_kwartiel:
                toplijst.append([gametimedict[game], gamenamedict[game]])

        self.sorteer_data(toplijst)
        self.sorteer_data(floplijst)

        text += "De top 10 meest gespeelde spellen zijn: \n(Als het er minder dan 10 zijn is het de top 25%.)\n"
        counter = 0
        for x in range(len(toplijst) - 1, 0, -1):
            if counter < 10:
                text += f"{toplijst[x][1]}, {int(toplijst[x][0] / 60 / 24)} dagen gespeeld\n"
                counter += 1
        if counter < 10:
            text += "Correctie: dit zijn de top 25% meest gespeelde spellen"
        text += "\n"
        text += "De top 10 minst gespeelde spellen zijn (niet gespeelde spellen uitgesloten):\n"
        counter = 0
        for x in range(0, len(floplijst) - 1):
            if counter < 10 and floplijst[x][0] > 0:
                text += f"{floplijst[x][1]}, {int(floplijst[x][0])} minuten gespeeld\n"
                counter += 1
        if counter == 0:
            text += "Er zitten geen games met meer dan 0 speelminuten in de onderste 25%."
        elif counter < 10:
            text += "Correctie: dit zijn de onderste 25% minst gespeelde spellen."
        text += "\n\n"
        if hoogste_game_user == username:
            hoogste_game_user = "jijzelf"
        if hoogste_speeltijd_user == username:
            hoogste_speeltijd_user = "jijzelf"
        text += f"Je rijkste vriend is {hoogste_game_user}, deze heeft {hoogste_game_aantal} games.\n"
        text += f"Je meest levenloze vriend is {hoogste_speeltijd_user}, deze heeft " \
                f"{gamenamedict[hoogste_speeltijd_appid]} {hoogste_speeltijd} minuten gespeeld! " \
                f"(Dat is {int(hoogste_speeltijd / 60 / 24)} dagen!) "

        self.text.insert(INSERT, text)
        self.text.configure(state=DISABLED)

    def sorteer_data(self, data):
        quicksort = Quicksort(data)
        quicksort.quicksortRecusrive(data, 0, len(data) - 1)
        """ Deze funtie sorteert de ingevoerde data."""
