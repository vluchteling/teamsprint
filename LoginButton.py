import time
import RPi.GPIO as GPIO
import gevent
from gevent.exceptions import LoopExit

from SteamClientAPI import SteamClientAPI
import atexit


class LoginButton:
    def __init__(self, steamgui, client):
        self.led = 18
        self.knopuno = 23
        self.loggedin = True
        self.client = client
        self.username, self.password = self.client.get_credentials()
        self.SteamGUI = steamgui
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(self.knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.knopuno, GPIO.RISING, callback=self.login_checker)
        GPIO.output(self.led, GPIO.HIGH)
        atexit.register(self.lights_out)

    def login_checker(self, twentythree):

        if GPIO.input(self.knopuno):

            if self.loggedin:

                while True:
                    print("iteratie")
                    try:
                        if self.client is not None:
                            self.client.log_out()
                        self.client = None
                        break

                    except LoopExit:
                        print("loopexit")
                        continue

                print("u wordt uitgelogd.")
                GPIO.output(self.led, GPIO.LOW)
                self.loggedin = False

                self.SteamGUI.set_client(None)





            else:
                print("u wordt ingelogd.")
                GPIO.output(self.led, GPIO.HIGH)
                self.loggedin = True
                self.client = SteamClientAPI(self.username, self.password)
                self.client.open_client()
                self.SteamGUI.set_client(self.client)
        gevent.sleep(1)

    def lights_out(self):
        GPIO.output(self.led, GPIO.LOW)
