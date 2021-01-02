import os
from tkinter import *
from tkinter.font import Font
from SteamWebAPI import SteamWebAPI
from LoginButton import LoginButton
from SteamClientAPI import SteamClientAPI


class SteamGUI:
    def __init__(self):
        self.client = None
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
        self.Button = LoginButton(self)
        self.start()

    def quit(self):
        """ Deze functie sluit de applicatie af. """
        self.root.destroy()
        raise SystemExit

    def display_owned_games(self, steamid):
        """ Deze functie geeft de naam van het eerste spel uit het bronbestand weer."""

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


SteamGUI()
