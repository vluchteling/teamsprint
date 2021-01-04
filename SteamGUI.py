import os
from tkinter import *
from tkinter.font import Font
from SteamWebAPI import SteamWebAPI
from LoginButton import LoginButton
from Servo import Servo
from Schuifregister import Schuifregister
from EchoSensor import Sr04
#from Neopixel import Neopixel


class SteamGUI:
    def __init__(self, client):
        self.client = client
        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi

        # De GUI code
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        groot_font = Font(size=30)
        self.root.configure(bg="#2f2c2f")
        self.titelframe = Label(font=groot_font, background="#5a565a", text="Titel van het eerste spel:")
        self.naamframe = Label(font=groot_font, background="#5a565a")
        self.afsluitButton = Button(text="Afsluiten", command=self.quit,
                                    background="#5a565a", foreground="white", font=groot_font)
        self.afsluitButton.pack(side=BOTTOM, pady=5)
        self.titelframe.pack(side=TOP, pady=30)
        self.naamframe.pack(side=TOP, pady=5)
        #self.servo()
        Schuifregister()
        self.Button = LoginButton(self, self.client)
        self.display_owned_games(steamid=self.client.get_client().steam_id.as_64)
        #self.sr04 = Sr04()
        #self.sr04.start()



        self.start()

    def quit(self):
        """ Deze functie sluit de applicatie af. """
        self.root.destroy()
        raise SystemExit

    def servo(self):
        servo = Servo()
        servo.start_spel()

    """def speel_bericht(self):
        neopixel = Neopixel()
        neopixel.speel_berichtanimatie()"""

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
        """ Deze funtie sorteert de ingevoerde data."""
        return sorted(data)

    def start(self):
        self.root.mainloop()

    def set_client(self, client):
        self.client = client
        if self.client is not None:
            self.display_owned_games(self.client.steam_id.as_64)
        else:
            self.display_owned_games(None)

