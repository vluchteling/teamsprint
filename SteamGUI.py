from tkinter import *
from tkinter.font import Font
from SteamWebAPI import SteamWebAPI


class SteamGUI:
    def __init__(self, parent):
        groot_font = Font(size="30")
        # De GUI code
        self.root = parent
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#2f2c2f")
        self.titelframe = Label(font=groot_font, background="#5a565a", text="Titel van het eerste spel:")
        self.naamframe = Label(font=groot_font, background="#5a565a")
        self.afsluitButton = Button(text="Afsluiten", command=self.quit,
                                    background="#5a565a", foreground="white", font=groot_font)
        self.afsluitButton.pack(side=BOTTOM, pady=5)
        self.display_owned_games()
        self.titelframe.pack(side=TOP, pady=30)
        self.naamframe.pack(side=TOP, pady=5)

    def quit(self):
        """ Deze functie sluit de applicatie af. """
        self.root.destroy()
        return

    def display_owned_games(self):
        """ Deze functie geeft de naam van het eerste spel uit het bronbestand weer."""
        steamid = 76561197995118880
        data = SteamWebAPI().get_steam_games_from_user(steamid)
        self.naamframe["text"] = data["response"]["games"][0]["name"]

    def sorteer_data(self, data):
        """ Deze funtie sorteert de ingevoerde data."""
        return sorted(data)


root = Tk()
myapp = SteamGUI(root)
root.mainloop()
