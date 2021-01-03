import os
from tkinter import *
from tkinter.font import Font
from SteamClientAPI import SteamClientAPI
from SteamGUI import SteamGUI


class Beginscherm():
    def __init__(self):
        if os.environ.get('DISPLAY', '') == '':
            os.environ.__setitem__('DISPLAY', ':0.0')  # Fix voor raspberrypi

        # De GUI code
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.groot_font = Font(size=30)
        self.root.configure(bg="#2f2c2f")
        self.user_label = Label(font=self.groot_font, background="#5a565a", text="username:")
        self.user_entry = Entry(width=35)
        self.password_label = Label(font=self.groot_font, background="#5a565a", text="password")
        self.password_entry = Entry(width=35)
        self.password_entry.configure(show="*")
        afsluitButton = Button(text="Afsluiten", command=self.quit,
                                    background="#5a565a", foreground="white", font=self.groot_font)
        self.bevestigButton = Button(text="Bevestig", command=self.start_client,
                                     background="#5a565a", foreground="white", font=self.groot_font)
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
        raise SystemExit

    def start_client(self):
        if self.password_entry.get().strip() != "" and self.user_entry.get().strip() != "":
            username = self.user_entry.get()
            password = self.password_entry.get()
            self.root.destroy()
            client = SteamClientAPI(username, password)
            client.open_client()
            SteamGUI(client)


        else:
            self.user_label["text"] = "lege velden!\nusername:"





Beginscherm()
