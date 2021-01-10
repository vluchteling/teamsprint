import os
import time
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from gevent.exceptions import LoopExit
from steam.client.user import SteamUser
from SteamClientAPI import SteamClientAPI
from SteamWebAPI import SteamWebAPI
from LoginButton import LoginButton
from Servo import Servo
from Schuifregister import Schuifregister
from EchoSensor import Sr04
from Neopixel import Neopixel


class SteamGUI:
    def __init__(self, client):

        self.client = client
        self.username, self.password = self.client.get_credentials()
        self.root = None
        self.button = None
        self.sr04 = None
        self.Button = None
        self.api = SteamWebAPI()
        self.servo = Servo()

        self.loginbutton = LoginButton(self)
        self.sr04 = Sr04(self.client, self)
        self.sr04.start()
        self.open_gui()

    def stuur_bericht(self, steam_id, text):
        print(text)
        self.client.get_client().get_user(steam_id).send_message(text)
        neopixel = Neopixel()
        neopixel.speel_berichtanimatie()

    def open_gui(self):
        try:
            if os.environ.get('DISPLAY', '') == '':
                os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi

            # De GUI code
            self.root = Tk()
            self.root.attributes("-fullscreen", True)
            groot_font = Font(size=30)
            self.root.configure(bg="#2f2c2f")
            self.titelframe = Label(font=groot_font, background="#5a565a", text="Titel van het eerste spel:")
            self.naamframe = Label(font=groot_font, background="#5a565a")
            self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                        background="#5a565a", foreground="white", font=groot_font)
            berichtframe = Frame()
            self.user_label = Label(berichtframe, font=groot_font, background="#5a565a", text="stel favoriet in")
            self.msg_button = Button(berichtframe, text="stel in", command=self.check_online,
                                     background="#5a565a", foreground="white", font=groot_font)
            self.afsluitButton.pack(side=BOTTOM, pady=5)
            self.titelframe.pack(side=TOP, pady=30)
            self.naamframe.pack(side=TOP, pady=5)
            self.friendframe = Frame()
            berichtframe.pack(side=RIGHT)
            self.user_label.pack()
            self.msg_button.pack()
            self.friendframe.pack(side=LEFT)
            self.display_owned_games(steamid=self.client.get_client().steam_id.as_64)
            self.toon_friendlist()
            self.root.mainloop()
        except:
            self.stop()

    def toon_friendlist(self):
        data = self.api.get_friend_list(steamid=self.client.get_client().steam_id.as_64)
        online = 0
        friendlist = []
        try:
            friendjson = data['friendslist']['friends']
            print(friendjson)
            friend = friendjson[0]['steamid']
            gameslst = self.api.get_steam_games_from_user(friend)
            appid = gameslst['response']['games'][0]['appid']
            data2 = self.api.get_procent(Appid=appid)

            percentages = data2['achievementpercentages']['achievements']

            leeglst = []
            for percentage in percentages:
                leeglst.append(percentage['percent'])
            print(self.sorteer_data(leeglst))

            for friend in friendjson:
                try:
                    games = self.api.friendstatus(friend['steamid'])
                    status = games['response']['players'][0]['personastate']
                    naam = games['response']['players'][0]['personaname']
                    if not (status == 0 or status == 7):
                        online += 1
                    friendlist.append([naam, status, friend['steamid']])
                except KeyError:
                    print(f"deze gebruiker is een zwerver")
        except KeyError:
            print("Deze gebruiker is een zwerver.")
        print(f"Aantal vrienden online: {online}")
        koppen = ('Naam', 'Status')
        self.treeview = ttk.Treeview(self.friendframe, columns=koppen, show='headings', )
        scrollbar = Scrollbar(self.friendframe)
        self.treeview.config(yscrollcommand=scrollbar.set)
        for col in koppen:
            self.treeview.heading(col, text=col)
        friendlist = self.sorteer_data(friendlist)

        for friend in friendlist:
            self.treeview.insert("", "end",
                            values=(friend[0], friend[1], friend[2]))

        self.treeview.pack()
        scrollbar.config(command=self.treeview.yview)
        #scrollbar.pack()

    def start_sensoren(self):
        Schuifregister()

    def stop(self):
        """ Deze functie sluit de applicatie af. """
        if self.root is not None:
            self.root.destroy()
            self.root = None
        try:
            self.sr04.stop()
        except AttributeError:
            pass

    def check_online(self):
        curItem = self.treeview.focus()
        friend = self.treeview.item(curItem)['values'][2]
        data = self.api.friendstatus(friend)
        status = data['response']['players'][0]['personastate']
        if status == 0:
            self.servo.start_spel(0)
            print("offline")
        else:
            self.servo.start_spel(1)
            print("online")

    def display_owned_games(self, steamid):
        """ Deze functie geeft de naam van het eerste spel uit het bronbestand weer."""
        if steamid is None:
            self.naamframe["text"] = "Uitgelogd."
            return

        data = SteamWebAPI().get_steam_games_from_user(steamid)
        try:
            self.naamframe["text"] = data["response"]["games"][0]["name"]
        except KeyError:
            self.naamframe["text"] = "Deze gebruiker heeft geen games."

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
        return (kleinste + 1)

    def quicksort(self, lst, min, max):
        if min < max:
            pi = self.partition(lst, min, max)
            self.quicksort(lst, min, pi - 1)
            self.quicksort(lst, pi + 1, max)

    def log_out(self):
        self.stuur_bericht(76561197995118880, "Ik ga, later man.")
        while True:
            try:
                self.client.log_out()
                break
            except LoopExit:
                continue
        self.client = None
        self.sr04.stop()
        self.display_owned_games(None)

    def log_in(self):
        self.client = SteamClientAPI(self.username, self.password)
        self.client.open_client()
        self.sr04 = Sr04(self.client, self)
        self.sr04.start()
        self.display_owned_games(self.client.get_client().steam_id.as_64)
        self.stuur_bericht(76561197995118880, "Yo, alles goed?")
