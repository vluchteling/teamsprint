import os
from tkinter import *
from tkinter.font import Font

from PIL import ImageTk

from SteamClientAPI import SteamClientAPI
from SteamGUI import SteamGUI


class Beginscherm:
    def __init__(self):
        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi

        # De GUI code
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.groot_font = Font(size=30)
        bg = ImageTk.PhotoImage(file='pexels-photo-2763927.jpg')
        background_label = Label(image=bg)
        background_label.image = bg
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.loginframe = Frame(height=110, bd=0, bg="#8B008B")
        self.user_label = Label(font=self.groot_font,foreground="white", background="#4B0082", text="Gebruikersnaam:")
        self.user_entry = Entry(width=35)
        self.password_label = Label(font=self.groot_font,foreground="white", background="#4B0082", text="Wachtwoord:")
        self.password_entry = Entry(width=35)
        self.password_entry.configure(show="*")
        afsluitButton = Button(text="Afsluiten", command=self.quit,
                               background="#4B0082", foreground="white", font=self.groot_font)
        self.bevestigButton = Button(text="Bevestig", command=self.start_client,
                                     background="#4B0082", foreground="white", font=self.groot_font)
        self.loginframe.pack(side=TOP)
        afsluitButton.pack(side=BOTTOM, pady=5)
        self.user_label.pack(side=TOP, pady=30)
        self.user_entry.pack(side=TOP, pady=30)
        self.password_label.pack(side=TOP, pady=30)
        self.password_entry.pack(side=TOP, pady=30)
        self.bevestigButton.pack()
        self.root.mainloop()

    def quit(self):
        """ Deze functie sluit de applicatie af. """
        self.root.destroy()

    def start_client(self):
        if self.password_entry.get().strip() != "" and self.user_entry.get().strip() != "":
            username = self.user_entry.get().lower()
            password = self.password_entry.get()

            client = SteamClientAPI(username, password)
            result = client.open_client(root=self.root, beginscherm=self)

            if result == "ok":
                if self.root is not None:
                    self.root.destroy()
                self.root = None
                self.open_GUI(client)
            elif result == "password":
                self.user_label["text"] = "Verkeerde gegevens!\nUsername:"
            elif result == "unavailable":
                self.user_label["text"] = "Steam offline, probeer later opnieuw.\nUsername:"
            else:
                self.user_label["text"] = "Overige fout, neem contact op met de ontwikkelaar.\nUsername:"

        else:
            self.user_label["text"] = "lege velden!\nUsername:"

    def open_GUI(self, client):
        SteamGUI(client)


Beginscherm()
