import multiprocessing

from Neopixel import Neopixel


class Berichtverstuurder:
    def __init__(self, bericht, steam_id, client):
        self.bericht = bericht
        self.steam_id = steam_id
        self.client = client
        self.proc = multiprocessing.Process(target=self.stuur_bericht)

    def start(self):
        self.proc.start()

    def stuur_bericht(self):
        print(self.bericht)
        if self.steam_id != "begin" and self.steam_id is not None and self.client is not None:
            self.client.get_client().get_user(self.steam_id).send_message(self.bericht)
            neopixel = Neopixel()
            neopixel.speel_berichtanimatie()
