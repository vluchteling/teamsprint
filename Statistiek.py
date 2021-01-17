from tkinter import *
from tkinter.font import Font
from urllib.error import HTTPError

from SteamWebAPI import SteamWebAPI


class Statistiek:
    def __init__(self, client, root, gui):
        self.client = client
        self.root = root
        self.gui = gui
        self.groot_font = Font(size=30)
        self.datalabel = Label(font=self.groot_font, background="#5a565a", text="")

        self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                    background="#5a565a", foreground="white", font=self.groot_font)
        self.afsluitButton.pack(side=BOTTOM, pady=5)
        self.datalabel.pack(side=TOP, expand=1)
        self.webapi = SteamWebAPI()
        self.start_statistiek()

    def stop(self):
        self.afsluitButton.forget()
        self.datalabel.forget()

    def start_statistiek(self):
        username = self.client.get_client().user.name

        text = f"Hallo, {username}.\n"
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
        if friendjson is not None:
            for friend in friendjson:
                friendid = int(friend['steamid'])
                useridlist.append(friendid)

        #print(useridlist)
        gamesdata = None
        gamesdict = {}
        gamelist = []
        for user in useridlist:
            gamesdata = self.webapi.get_steam_games_from_user(user)
            try:
                gamesjson = gamesdata["response"]["games"]
            except KeyError:
                pass
            for game in gamesjson:
                gamelist.append(game["name"])

        #print(gamelist)
        achievementsdict = {}
        percentagelijst = []
        percentagetotaal = 0
        percentageaantal = 0
        for game in gamelist:
            try:

                data = self.webapi.get_procent(game)
                percentages = data["achievementpercentages"]["achievements"]
                for percentage in percentages:
                    percentagelijst.append(percentage['percent'])
                    percentagetotaal += percentage['percent']
                    percentageaantal += 1
                    achievementsdict[game] = percentagelijst
            except HTTPError:
                pass
        percentagemiddeld = percentagetotaal / percentageaantal
        text += f"Jij en je vrienden hebben gemiddeld: {percentagemiddeld}% van jullie achievements gehaald.\n"
        meestgespeeld = 0
        meestgespeeldnaam = "geen"
        minstgespeeld = 0
        minstgespeeldnaam = "geen"
        for game in achievementsdict:
            print(game)
        self.datalabel["text"] = text
