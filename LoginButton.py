import time
import RPi.GPIO as GPIO
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
        atexit.register(GPIO.cleanup)

    def login_checker(self, twentythree):
        print(twentythree)
        if GPIO.input(self.knopuno):
            if self.loggedin:
                print("u wordt uitgelogd.")
                GPIO.output(self.led, GPIO.LOW)
                self.loggedin = False
                self.client = None
                self.SteamGUI.set_client(None)
                time.sleep(1)

            else:
                print("u wordt ingelogd.")
                GPIO.output(self.led, GPIO.HIGH)
                self.loggedin = True
                self.client = SteamClientAPI(self.username, self.password)
                self.client.open_client()
                self.SteamGUI.set_client(self.client.get_client())
                time.sleep(1)

