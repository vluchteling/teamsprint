from tkinter import *
from tkinter.font import Font

from SteamWebAPI import SteamWebAPI


class Statistiek:
    def __init__(self, client, root, gui):
        self.client = client
        self.root = root
        self.gui = gui
        self.klein_font = Font(size=20)
        self.groot_font = Font(size=30)
        self.dataframe = Frame()
        scrollbar = Scrollbar(root)
        self.text = Text(root, font=self.klein_font, wrap=WORD,
                         yscrollcommand=scrollbar.set, background="#2f2c2f", bd=0)
        self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                    background="#5a565a", foreground="white", font=self.groot_font)
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
            for game in gamesjson:
                gametimedict[game["appid"]] = gametimedict.get(game["appid"], 0) + game["playtime_forever"]
                gamenamedict[game["appid"]] = game["name"]
        meest_gespeeld_appid = None
        hoogste_tijd = 0
        for game in gametimedict:
            if gametimedict[game] > hoogste_tijd:
                meest_gespeeld_appid = game
                hoogste_tijd = gametimedict[game]
        text += f"Het meest gespeelde spel is {gamenamedict[meest_gespeeld_appid]}. Dit is {int(hoogste_tijd / 60 / 24)} dagen gespeeld!\n"
        values = gametimedict.values()
        tijdenlist = []
        for item in values:
            tijdenlist.append(item)
        eerste_kwartiel = self.q1(tijdenlist)
        derde_kwartiel = self.q3(tijdenlist)
        toplijst = []
        floplijst = []
        for game in gametimedict:
            if gametimedict[game] < eerste_kwartiel:
                floplijst.append([gametimedict[game], gamenamedict[game]])
            elif gametimedict[game] > derde_kwartiel:
                toplijst.append([gametimedict[game], gamenamedict[game]])

        toplijst = self.sorteer_data(toplijst)
        floplijst = self.sorteer_data(toplijst)

        text += "De top 10 meest gespeelde spellen zijn:\n"
        counter = 0
        for x in range(len(toplijst) - 1, 0, -1):
            if counter < 10:
                text += f"{toplijst[x][1]}, {int(toplijst[x][0] / 60 / 24)} dagen gespeeld\n"
                counter += 1
        text += "\n"
        text += "De top 10 minst gespeelde spellen zijn (niet gespeelde spellen uitgesloten):\n"
        counter = 0
        for x in range(0, len(floplijst) - 1):
            if counter < 10:
                text += f"{floplijst[x][1]}, {int(floplijst[x][0])} minuten gespeeld\n"
                counter += 1
        text += "\n\n"
        text += f"Je rijkste vriend is {hoogste_game_user}, deze heeft {hoogste_game_aantal} games.\n"
        text += f"Je meest levenloze vriend is {hoogste_speeltijd_user}, deze heeft " \
                f"{gamenamedict[hoogste_speeltijd_appid]} {hoogste_speeltijd} minuten gespeeld! " \
                f"(Dat is {int(hoogste_speeltijd / 60 / 24)} dagen!) "

        self.text.insert(INSERT, text)
        self.text.configure(state=DISABLED)

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

    def partitionIterative(self, arr, l, h):
        i = (l - 1)
        x = arr[h]

        for j in range(l, h):
            if arr[j] <= x:
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[h] = arr[h], arr[i + 1]
        return (i + 1)

    def quickSortIterative(self, arr, l, h):

        # Create an auxiliary stack
        size = h - l + 1
        stack = [0] * (size)

        # initialize top of stack
        top = -1

        # push initial values of l and h to stack
        top = top + 1
        stack[top] = l
        top = top + 1
        stack[top] = h

        # Keep popping from stack while is not empty
        while top >= 0:

            # Pop h and l
            h = stack[top]
            top = top - 1
            l = stack[top]
            top = top - 1

            # Set pivot element at its correct position in
            # sorted array
            p = self.partitionIterative(arr, l, h)

            # If there are elements on left side of pivot,
            # then push left side to stack
            if p - 1 > l:
                top = top + 1
                stack[top] = l
                top = top + 1
                stack[top] = p - 1

            # If there are elements on right side of pivot,
            # then push right side to stack
            if p + 1 < h:
                top = top + 1
                stack[top] = p + 1
                top = top + 1
                stack[top] = h

    def sorteer_data(self, data):
        self.quickSortIterative(data, 0, len(data) - 1)
        """ Deze funtie sorteert de ingevoerde data."""
        return data

    def median(self, lst):
        """ Retourneer de mediaan (float) van de lijst lst. """
        lst = self.sorteer_data(lst)
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
        lst = self.sorteer_data(lst)
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
        lst = self.sorteer_data(lst)
        med = self.median(lst)
        sublijst = []
        for x in range(len(lst) - 1, 0, -1):
            if lst[x] > med:
                sublijst.append(lst[x])
            if lst[x] == med and lst[x - 1] == lst[x]:
                sublijst.append(lst[x])
        return self.median(sublijst)
