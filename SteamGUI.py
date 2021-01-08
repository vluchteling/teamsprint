import os
from tkinter import *
from tkinter.font import Font
from SteamWebAPI import SteamWebAPI
#from LoginButton import LoginButton
#from Servo import Servo
#from Schuifregister import Schuifregister
#from EchoSensor import Sr04
#from Neopixel import Neopixel


class SteamGUI:
    def __init__(self, client):
        try:
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
            #self.sr04 = Sr04()
            #self.sr04.start()
            #self.servo()
            #neopixel = Neopixel()
            #neopixel.speel_berichtanimatie()
            #Schuifregister()
            #self.Button = LoginButton(self, self.client)
            #self.display_owned_games(steamid=self.client.get_client().steam_id.as_64)
            self.api = SteamWebAPI()
            data = self.api.get_friend_list(steamid=self.client.get_client().steam_id.as_64)


            try:
                friendlist = data['friendslist']['friends']
                print(friendlist)
                friend = friendlist[0]['steamid']
                gameslst=self.api.get_steam_games_from_user(friend)
                appid= gameslst['response']['games'][0]['appid']
                data2 = self.api.get_procent(Appid=appid)
                #print(data2)

                percentages=data2['achievementpercentages']['achievements']
                #print(percentages)

                leeglst=[]
                for percentage in percentages:
                    #print(percentage)
                    #print(percentage['percent'])
                    dict=percentage
                    print(list(dict.keys()))
                    print(list(dict.values()))
                    print(list)
                    print(percentage.keys())
                    print(percentage.values())
                    #leegldicst = []
                    #leeglst.append(percentage)
                    #print(type(leeglst))
                    #print(sorted(leeglst))
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
                        print(f"{naam}: zwerver")
            except KeyError:
                print("Deze gebruiker is een zwerver.")

            """if test == "76561197995118880":
                print("hallo Adil")"""

            self.start()



        except:
            self.quit()

    def quit(self):
        """ Deze functie sluit de applicatie af. """
        self.root.destroy()
        #self.sr04.stop()
        quit()

    """def servo(self):
        servo = Servo()
        servo.start_spel()"""

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
