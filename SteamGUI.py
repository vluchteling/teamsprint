import os
import time
from tkinter import *
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

        # self.client.change_personastate("afwezig")

        self.toon_friendlist()
        self.loginbutton = LoginButton(self)
        self.sr04 = Sr04(self.client, self)
        self.sr04.start()
        self.open_gui()

    def stuur_bericht(self, steam_id, text):
        print(text)
        self.client.get_client().get_user(steam_id).send_message(text)
        neopixel = Neopixel()
        neopixel.speel_berichtanimatie()

    def toon_friendlist(self):
        data = self.api.get_friend_list(steamid=self.client.get_client().steam_id.as_64)

        try:
            friendlist = data['friendslist']['friends']
            print(friendlist)
            friend = friendlist[0]['steamid']
            gameslst = self.api.get_steam_games_from_user(friend)
            appid = gameslst['response']['games'][0]['appid']
            data2 = self.api.get_procent(Appid=appid)
            # print(data2)

            percentages = data2['achievementpercentages']['achievements']

            # print(percentages)

            leeglst = []
            for percentage in percentages:
                leeglst.append(percentage['percent'])
            print(self.sorteer_data(leeglst))

            for friend in friendlist:
                try:
                    games = self.api.friendstatus(friend['steamid'])
                    status = games['response']['players'][0]['personastate']
                    naam = games['response']['players'][0]['personaname']
                    if status == 0:
                        print(f"{naam}: offline")
                    elif status == 1:
                        print(f"{naam}: online")
                    elif status == 3:
                        print(f"{naam}: afwezig")
                    else:
                        print(f"{naam}: iets anders")
                except KeyError:
                    print(f"deze gebruiker is een zwerver")
        except KeyError:
            print("Deze gebruiker is een zwerver.")

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
            self.user_label = Label(berichtframe, font=groot_font, background="#5a565a", text="steamid_64 van vriend")
            self.user_entry = Entry(berichtframe)
            self.msg_button = Button(berichtframe, text="check", command=self.check_online,
                                     background="#5a565a", foreground="white", font=groot_font)
            self.afsluitButton.pack(side=BOTTOM, pady=5)
            self.titelframe.pack(side=TOP, pady=30)
            self.naamframe.pack(side=TOP, pady=5)

            berichtframe.pack(side=RIGHT)
            self.user_label.pack()
            self.user_entry.pack()
            self.msg_button.pack()
            self.display_owned_games(steamid=self.client.get_client().steam_id.as_64)
            self.root.mainloop()
        except:
            self.stop()

    def start_sensoren(self):

        self.sr04 = Sr04(self.client, self)
        self.sr04.start()
        neopixel = Neopixel()
        neopixel.speel_berichtanimatie()
        Schuifregister()
        self.Button = LoginButton(self)

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
        friend = self.user_entry.get()
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

