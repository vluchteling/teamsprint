import os
from tkinter import *
from tkinter.font import Font

from steam.client.user import SteamUser

from SteamWebAPI import SteamWebAPI

from LoginButton import LoginButton
from Servo import Servo
from Schuifregister import Schuifregister
from EchoSensor import Sr04
from Neopixel import Neopixel


class SteamGUI:
    def __init__(self, client):

        self.client = client
        self.root = None
        self.button = None
        self.sr04 = None
        self.Button = None
        self.api = SteamWebAPI()
        #self.stuur_bericht(76561199119177557, "Yo Adil, alles goed?")
        self.sr04 = Sr04(self.client)
        self.sr04.start()
        #self.client.change_personastate("afwezig")

        self.toon_friendlist()
        self.open_gui()

    def stuur_bericht(self, steam_id, text):
        client = self.client.get_client()
        adil = client.get_user(steam_id)
        adil.send_message(text)
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
            self.afsluitButton.pack(side=BOTTOM, pady=5)
            self.titelframe.pack(side=TOP, pady=30)
            self.naamframe.pack(side=TOP, pady=5)
            self.display_owned_games(steamid=self.client.get_client().steam_id.as_64)
            self.root.mainloop()
        except:
            self.stop()

    def start_sensoren(self):

        self.sr04 = Sr04()
        self.sr04.start()
        servo = Servo()
        servo.start_spel()
        neopixel = Neopixel()
        neopixel.speel_berichtanimatie()
        Schuifregister()
        self.Button = LoginButton(self, self.client)

    def stop(self):
        """ Deze functie sluit de applicatie af. """
        if self.root is not None:
            self.root.destroy()
            self.root = None
        self.sr04.stop()

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
        self.quickSort(data, 0, len(data) - 1)
        """ Deze funtie sorteert de ingevoerde data."""
        return data

    # Python program for implementation of Quicksort Sort

    # This function takes last element as pivot, places
    # the pivot element at its correct position in sorted
    # array, and places all smaller (smaller than pivot)
    # to left of pivot and all greater elements to right
    # of pivot
    def partition(self, arr, low, high):
        i = (low - 1)  # index of smaller element
        pivot = arr[high]  # pivot

        for j in range(low, high):

            # If current element is smaller than the pivot
            if arr[j] < pivot:
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

        # The main function that implements QuickSort

    # arr[] --> Array to be sorted,
    # low --> Starting index,
    # high --> Ending index

    # Function to do Quick sort
    def quickSort(self, arr, low, high):
        if low < high:
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = self.partition(arr, low, high)

            # Separately sort elements before
            # partition and after partition
            self.quickSort(arr, low, pi - 1)
            self.quickSort(arr, pi + 1, high)

            # Driver code to test above

    def set_client(self, client):
        self.client = client
        if self.client is not None:
            self.display_owned_games(self.client.steam_id.as_64)
        else:
            self.display_owned_games(None)
