import os
import threading
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from urllib.error import HTTPError

from PIL import ImageTk
from gevent.exceptions import LoopExit

from Grafieken import DataScherm
from EchoSensor import Sr04
from Loginbutton import LoginButton
from Neopixel import Neopixel
from Quicksort import Quicksort
from Schuifregister import Schuifregister
from Servo import Servo
from Statistiek import Statistiek
from SteamClientAPI import SteamClientAPI
from SteamWebAPI import SteamWebAPI


class SteamGUI:
    def __init__(self, client):
        """ Init functie van de class"""

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
        self.selecteditem = None
        self.runfriendlist = True
        self.runonline = True
        self.loginbutton = None
        self.neopixel = None
        self.onlinetimer = None
        self.friendlist_timer = None
        self.databutton = None
        self.statistiekbutton = None
        self.servobuttonframe = None
        self.collijst = None
        self.needs2bsorted = False
        self.api = SteamWebAPI()

        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.open_gui(True)
        self.start_sensoren(True)
        self.start_gui()

    def open_gui(self, stopbutton):
        """ Deze functie laadt de gui objecten in."""

        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi

        self.groot_font = Font(size=30)
        bg = ImageTk.PhotoImage(file='pexels-photo-2763927.jpg')
        background_label = Label(image=bg)
        background_label.image = bg
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        bgcolor = "#4B0082"

        self.titelframe = Label(font=self.groot_font, background=bgcolor, foreground="white", text="SteamPI Client")
        self.databutton = Button(text="Data", command=self.open_data,
                                 background=bgcolor, foreground="white", font=self.groot_font)
        self.statistiekbutton = Button(text="Statistiek", command=self.open_statistiek,
                                       background=bgcolor, foreground="white", font=self.groot_font)

        self.berichtframe = Frame(background=bgcolor)
        self.user_label = Label(self.berichtframe, font=self.groot_font, foreground="white", background=bgcolor,
                                text="Volg de status van een vriend.")
        self.favoriet_label = Label(self.berichtframe, foreground="white", font=self.groot_font, background=bgcolor,
                                    text="Huidige favoriet: Geen")
        self.servobuttonframe = Frame(self.berichtframe, background=bgcolor)
        self.msg_button = Button(self.servobuttonframe, text="Stel in", command=self.check_online,
                                 background=bgcolor, foreground="white", font=self.groot_font)
        self.clear_button = Button(self.servobuttonframe, text="Stop", command=self.timerstop,
                                   background=bgcolor, foreground="white", font=self.groot_font)
        if stopbutton:
            self.afsluitButton = Button(text="Afsluiten", command=self.stop,
                                        background=bgcolor, foreground="white", font=self.groot_font)
            self.afsluitButton.pack(side=BOTTOM, pady=5)
        self.titelframe.pack(side=TOP, pady=60, padx=30)

        self.servobuttonframe.pack(side=BOTTOM, expand=1, fill=X, pady=5)

        self.friendframe = Frame(self.berichtframe, background=bgcolor)
        self.berichtframe.pack(pady=30, padx=30)
        self.user_label.pack()
        self.favoriet_label.pack()
        self.msg_button.pack(side=LEFT)
        self.clear_button.pack(side=RIGHT)
        self.friendframe.pack()
        self.databutton.pack(side=RIGHT)
        self.statistiekbutton.pack(side=LEFT)

    def clear_gui(self, afsluitbutton):
        """ Deze functie maakt het scherm leeg. """
        if afsluitbutton:
            self.afsluitButton.forget()

        self.titelframe.forget()
        self.databutton.forget()
        self.statistiekbutton.forget()
        self.berichtframe.forget()
        self.user_label.forget()
        self.favoriet_label.forget()
        self.msg_button.forget()
        self.clear_button.forget()
        self.friendframe.forget()
        self.servobuttonframe.forget()
        if self.treeview is not None:
            self.treeview.forget()
            self.treeview = None

    def start_gui(self):
        """ Deze functie start de mainloop"""

        self.root.mainloop()

    def start_sensoren(self, loginbtnstart):
        """ Deze functie start de sensoren op, en vertraagt het programma"""
        self.runfriendlist = True
        self.runonline = True
        self.toon_friendlist()
        self.neopixel = Neopixel()
        self.neopixel.speel_loginanimatie()
        self.sr04 = Sr04(self.client, self.neopixel)
        self.sr04.start()

        if loginbtnstart:
            self.loginbutton = LoginButton(self)

    def stop_sensoren(self, loginbtndelete):
        """ Deze functie sluit alle sensoren af. """
        if self.neopixel is not None:
            self.neopixel.speel_loguitanimatie()
        if self.schuifregister is not None:
            self.schuifregister.lichtjes(0)
        self.favoriet = None
        self.runfriendlist = False
        self.runonline = False
        if self.onlinetimer is not None:
            self.onlinetimer.join(5)
            if self.schuifregister is not None:
                self.schuifregister.lichtjes(0)
        if self.friendlist_timer is not None:
            self.friendlist_timer.join(5)
        if self.sr04 is not None:
            self.sr04.stop()
        if loginbtndelete:
            if self.loginbutton is not None:
                self.loginbutton.lights_out()
                self.loginbutton = None

    def toon_friendlist(self):
        """ Deze functie laadt de vriendlijst uit steam,
         stopt hem in een treeview en herheelt dit iedere 10 seconden."""

        if self.runfriendlist:

            try:
                data = self.api.get_friend_list(steamid=self.client.get_client().steam_id.as_64)
            except HTTPError:
                return
            online = 0
            friendlist = []
            try:
                friendjson = data['friendslist']['friends']

                for friend in friendjson:
                    try:
                        games = self.api.friendstatus(friend['steamid'])
                        status = games['response']['players'][0]['personastate']
                        naam = games['response']['players'][0]['personaname']
                        if not (status == 0 or status == 7):
                            online += 1
                        if status == 0:
                            status = "Offline"
                        elif status == 1:
                            status = "Online"
                        elif status == 2:
                            status = "Bezig"
                        elif status == 3:
                            status = "Afwezig"
                        elif status == 4:
                            status = "Slapend"
                        elif status == 5:
                            status = "Ruilzoekende"
                        elif status == 6:
                            status = "Spelzoekende"
                        elif status == 7:
                            status = "Fake offline"
                        elif status == 8:
                            status = "max"
                        else:
                            status = "onbekend"
                        friendlist.append([naam, status, friend['steamid']])
                    except KeyError:
                        pass
            except KeyError:
                pass
            self.schuifregister = Schuifregister()
            self.schuifregister.lichtjes(online)
            if online != self.online:
                self.online = online
            koppen = ('Naam', 'Status')
            if self.treeview is not None:

                self.treeview.delete(*self.treeview.get_children())

            else:
                try:
                    self.treeview = ttk.Treeview(self.friendframe, columns=koppen, show='headings')
                except RuntimeError:
                    return
                scrollbar = Scrollbar(self.friendframe)
                self.treeview.config(yscrollcommand=scrollbar.set)
                self.treeview.pack(expand=1, fill=BOTH)
                scrollbar.config(command=self.treeview.yview)

            self.collijst = []
            for col in koppen:
                self.collijst.append(col)
                if self.treeview is not None:
                    self.treeview.heading(col, text=col,
                                          command=self.treeview_sort_column)
                else:
                    return
            self.sorteer_data(friendlist)

            if self.treeview is not None:
                for friend in friendlist:
                    self.treeview.insert("", "end",
                                         values=(friend[0], friend[1], friend[2]))
                if self.selecteditem is not None:
                    for i in self.treeview.get_children():
                        try:
                            if self.treeview.item(i)['values'][2] == self.favoriet:
                                self.treeview.focus(i)
                                self.treeview.selection_set(i)
                        except TclError:
                            pass
                self.sort_column_noclick()
                self.friendlist_timer = threading.Timer(10, self.toon_friendlist)
                self.friendlist_timer.deamon = True
                self.friendlist_timer.start()
            else:

                return

        else:
            return

    def stop(self):
        """ Deze functie sluit de applicatie af. """
        self.root.destroy()
        self.stop_sensoren(True)
        raise SystemExit

    def check_online(self):
        """ Deze functie volgt de geselecteerde gebruiker van de treeview, update iedere 2 seconden."""
        if self.favoriet is not None and self.treeview is not None and self.runonline:

            try:
                self.selecteditem = self.treeview.focus()
                if self.selecteditem == "":
                    return
            except IndexError:
                return
            self.afsluitButton.forget()
            try:
                friend_name = self.treeview.item(self.selecteditem)['values'][0]
            except IndexError:
                return
            except AttributeError:
                return
            except TclError:
                return
            favoriet = self.treeview.item(self.selecteditem)['values'][2]
            if self.favoriet != favoriet:
                self.favoriet = favoriet
            self.favoriet_label["text"] = f"Huidige favoriet: {friend_name}"
            servo = Servo()
            data = self.api.friendstatus(self.favoriet)
            status = data['response']['players'][0]['personastate']
            if status != self.status:
                servo.start_spel(status)
                self.status = status
            self.onlinetimer = threading.Timer(2, self.check_online)
            self.onlinetimer.deamon = True
            self.onlinetimer.start()
        elif self.favoriet is None and self.treeview is not None and not self.runonline:
            self.runonline = True
            self.favoriet_label["text"] = f"Huidige favoriet: geen"
            self.favoriet = "begin"
        else:
            return

    def log_out(self):
        """ Callback functie voor de button, logt de gebruiker uit en sluit alle sensoren af."""
        try:
            self.client.log_out()
        except LoopExit:
            pass
        self.clear_gui(False)
        self.stop_sensoren(False)
        if self.friendlist_timer is not None:
            self.friendlist_timer.join(5)
        if self.onlinetimer is not None:
            self.onlinetimer.join(5)
        self.client = None

    def log_in(self):
        """ Callback functie voor de button, logt de gebruiker in en start de gui + sensoren op"""
        self.neopixel.speel_loginanimatie()
        self.client = SteamClientAPI(self.username, self.password)
        self.client.open_client()
        self.favoriet = "begin"
        self.afsluitButton.forget()
        self.open_gui(True)
        self.start_sensoren(False)

    def timerstop(self):
        """ Deze fucntie stopt de check_gebruiker functie als er op de knop is gedrukt"""
        if self.selecteditem is None or self.selecteditem == "":
            return
        self.favoriet = "begin"
        self.runfriendlist = False
        if self.treeview is not None:
            self.treeview.forget()
        self.clear_gui(True)
        self.open_gui(True)
        if self.onlinetimer is not None:
            self.onlinetimer.join(5)
        self.runfriendlist = True
        self.toon_friendlist()
        self.runonline = True
        self.favoriet_label["text"] = f"Huidige favoriet: geen"

    def open_data(self):
        """ Deze functie opent het datascherm"""
        self.stop_sensoren(True)
        self.clear_gui(True)
        self.neopixel.lights_out()
        self.favoriet = "begin"
        DataScherm(self.client, self.root, self)

    def sorteer_data(self, data):
        """ Deze funtie sorteert de ingevoerde data."""
        quicksort = Quicksort(data)
        quicksort.quicksortRecusrive(data, 0, len(data) - 1)


    def treeview_sort_column(self):
        """Deze functie sorteert de koppen van de treeview als er op de kop is gedrukt"""
        koppenlijst = []
        for kop in self.treeview.get_children(''):
            koppenlijst.append(kop)
        copylijst = koppenlijst.copy()
        copylijst.reverse()
        for kop in koppenlijst:
            self.treeview.move(kop, '', copylijst.index(kop))
        self.needs2bsorted = not self.needs2bsorted

    def sort_column_noclick(self):
        """ Deze fucntie sorteert de kolommen als dat nodig is en de vriendlijst wordt refreshed."""

        koppenlijst = []

        for kop in self.treeview.get_children(''):
            koppenlijst.append(kop)
        copylijst = koppenlijst.copy()
        if self.needs2bsorted:
            copylijst.reverse()

        for kop in koppenlijst:
            self.treeview.move(kop, '', copylijst.index(kop))

    def open_statistiek(self):
        """ Deze functie opent het statistiekscherm"""
        self.stop_sensoren(True)
        self.clear_gui(True)
        self.neopixel.lights_out()
        self.favoriet = "begin"
        Statistiek(self.client, self.root, self)
