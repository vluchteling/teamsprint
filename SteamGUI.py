import _tkinter
import os
import threading
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

from gevent.exceptions import LoopExit

from AI import DataScherm
from EchoSensor import Sr04
from LoginButton import LoginButton
from Neopixel import Neopixel
from Schuifregister import Schuifregister
from Servo import Servo
from SteamClientAPI import SteamClientAPI
from SteamWebAPI import SteamWebAPI


class SteamGUI:
    def __init__(self, client):

        self.client = client
        self.username, self.password = self.client.get_credentials()

        self.root = None
        self.button = None
        self.sr04 = None
        self.Button = None
        self.servo = None
        self.favoriet = "begin"
        self.status = None
        self.onlinetimer = None
        self.friendtimer = None
        self.groot_font = None
        self.titelframe = None
        self.naamframe = None
        self.afsluitButton = None
        self.berichtframe = None
        self.user_label = None
        self.favoriet_label = None
        self.msg_button = None
        self.clear_button = None
        self.friendframe = None
        self.treeview = None
        self.online = None
        self.schuifregister = None

        self.api = SteamWebAPI()

        self.loginbutton = LoginButton(self)
        self.sr04 = Sr04(self.client, self, None)
        self.sr04.start()
        self.open_gui()

    def stuur_bericht(self, steam_id, text):
        print(text)
        if steam_id != "begin":
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
            self.groot_font = Font(size=30)
            self.root.configure(bg="#2f2c2f")
            self.titelframe = Label(font=self.groot_font, background="#5a565a", text="Titel van het eerste spel:")
            self.naamframe = Label(font=self.groot_font, background="#5a565a")
            self.databutton = Button(text="Afsluiten", command=self.open_data,
                                     background="#5a565a", foreground="white", font=self.groot_font)
            self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                        background="#5a565a", foreground="white", font=self.groot_font)
            self.berichtframe = Frame(background="#2f2c2f")
            self.user_label = Label(self.berichtframe, font=self.groot_font, background="#5a565a",
                                    text="stel favoriet in")
            self.favoriet_label = Label(self.berichtframe, font=self.groot_font, background="#5a565a",
                                        text="Huidige favoriet: Geen")
            self.msg_button = Button(self.berichtframe, text="Stel in", command=self.check_online,
                                     background="#5a565a", foreground="white", font=self.groot_font)
            self.clear_button = Button(self.berichtframe, text="Stop", command=self.timerstop,
                                       background="#5a565a", foreground="white", font=self.groot_font)
            self.afsluitButton.pack(side=BOTTOM, pady=5)
            self.titelframe.pack(side=TOP, pady=30)
            self.naamframe.pack(side=TOP, pady=5)
            self.databutton.pack()
            self.friendframe = Frame(background="#2f2c2f")
            self.berichtframe.pack(side=RIGHT)
            self.user_label.pack()
            self.favoriet_label.pack()
            self.msg_button.pack()
            self.clear_button.pack()
            self.friendframe.pack(side=LEFT)
            self.display_owned_games(steamid=self.client.get_client().steam_id.as_64)
            self.toon_friendlist()
            self.root.mainloop()
        except:
            self.stop()

    def toon_friendlist(self):
        try:
            data = self.api.get_friend_list(steamid=self.client.get_client().steam_id.as_64)
            online = 0
            friendlist = []
            try:
                friendjson = data['friendslist']['friends']

                for friend in friendjson:
                    try:
                        print(friend['steamid'])
                        games = self.api.friendstatus(friend['steamid'])
                        print(games)

                        status = games['response']['players'][0]['personastate']
                        naam = games['response']['players'][0]['personaname']
                        if not (status == 0 or status == 7):
                            online += 1
                        friendlist.append([naam, status, friend['steamid']])
                    except KeyError:
                        print(f"deze gebruiker is een zwerver")
            except KeyError:
                print("Deze gebruiker is een zwerver.")
            if online != self.online:
                self.schuifregister = Schuifregister()
                self.schuifregister.lichtjes(online)
                self.online = online
            koppen = ('Naam', 'Status')
            if self.treeview is not None:
                try:
                    self.treeview.forget()
                except _tkinter.TclError:
                    return
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
            self.friendtimer = threading.Timer(1, self.toon_friendlist).start()
        except RuntimeError:
            pass
        except AttributeError:
            print("ae")
            self.treeview.forget()




    def stop(self):
        """ Deze functie sluit de applicatie af. """
        if self.root is not None:
            self.root.destroy()
            self.root = None
        try:
            self.sr04.stop()
        except AttributeError:
            pass
        if self.servo is not None:
            self.servo.stop()
        if self.onlinetimer is not None:
            self.onlinetimer.cancel()
        if self.friendtimer is not None:
            self.friendtimer.cancel()

    def check_online(self):
        if self.favoriet is not None:
            curItem = self.treeview.focus()
            try:
                friend_name = self.treeview.item(curItem)['values'][0]
            except IndexError:
                return

            favoriet = self.treeview.item(curItem)['values'][2]
            self.favoriet = favoriet
            if self.sr04.get_vriend() is None:
                self.sr04.stop()
                self.sr04 = Sr04(self.client, self, self.favoriet)
                self.sr04.start()

            self.favoriet_label["text"] = f"Huidige favoriet: {friend_name}"
            servo = Servo()
            data = self.api.friendstatus(self.favoriet)
            status = data['response']['players'][0]['personastate']
            if status != self.status:
                servo.start_spel(status)
                self.status = status
            self.onlinetimer = threading.Timer(1, self.check_online).start()
        else:
            if self.onlinetimer is not None:
                self.onlinetimer.cancel()
            self.favoriet_label["text"] = f"Huidige favoriet: geen"
            self.favoriet = "begin"

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


    def log_out(self):
        if self.favoriet:
            self.stuur_bericht(self.favoriet, "Ik ga, later man.")
        while True:
            try:
                self.client.log_out()
                break
            except LoopExit:
                continue
        self.client = None
        self.sr04.stop()

        if self.servo is not None:
            self.servo.stop()
        if self.schuifregister is not None:
            self.schuifregister.lichtjes(0)
        if self.onlinetimer is not None:
            self.onlinetimer.cancel()
        if self.friendtimer is not None:
            self.friendtimer.cancel()
        self.display_owned_games(None)
        self.user_label.forget()
        self.favoriet_label.forget()
        self.msg_button.forget()
        self.treeview.forget()
        self.clear_button.forget()
        self.favoriet = None

    def log_in(self):
        self.client = SteamClientAPI(self.username, self.password)
        self.client.open_client()
        self.sr04 = Sr04(self.client, self, self.favoriet)
        self.sr04.start()
        self.display_owned_games(self.client.get_client().steam_id.as_64)
        self.user_label = Label(self.berichtframe, font=self.groot_font, background="#5a565a", text="stel favoriet in")
        self.favoriet_label = Label(self.berichtframe, font=self.groot_font, background="#5a565a",
                                    text="Huidige favoriet: Geen")
        self.msg_button = Button(self.berichtframe, text="Stel in", command=self.check_online,
                                 background="#5a565a", foreground="white", font=self.groot_font)
        self.clear_button = Button(self.berichtframe, text="Stop", command=self.timerstop,
                                   background="#5a565a", foreground="white", font=self.groot_font)
        self.user_label.pack()
        self.favoriet_label.pack()
        self.msg_button.pack()
        self.clear_button.pack()
        self.toon_friendlist()
        self.favoriet = "begin"

    def timerstop(self):
        self.favoriet = None
        self.favoriet_label["text"] = f"Huidige favoriet: geen"
        self.sr04.stop()

    def open_data(self):
        self.afsluitButton.forget()
        self.titelframe.forget()
        self.naamframe.forget()
        self.databutton.forget()
        self.berichtframe.forget()
        self.user_label.forget()
        self.favoriet_label.forget()
        self.msg_button.forget()
        self.clear_button.forget()
        self.friendframe.forget()
        self.treeview.forget()
        self.schuifregister.lichtjes(0)
        self.friendtimer.cancel()
        self.friendtimer = None
        DataScherm(self.client, self.root)

        self.open_gui()
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
