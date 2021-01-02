import RPi.GPIO as GPIO
from SteamClientAPI import SteamClientAPI


class LoginButton:
    def __init__(self, steamgui):
        self.led = 18
        self.knopuno = 23
        self.loggedin = False
        self.client = None
        self.SteamGUI = steamgui
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(self.knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.knopuno, GPIO.RISING, callback=self.login_checker)

    def login_checker(self, twentythree):
        print(twentythree)
        if GPIO.input(self.knopuno):
            if self.loggedin:
                print("u wordt uitgelogd.")
                GPIO.output(self.led, GPIO.LOW)
                self.loggedin = False
                self.client.log_out()
                self.client = None
                self.SteamGUI.set_client(None)

            else:
                print("u wordt ingelogd.")
                GPIO.output(self.led, GPIO.HIGH)
                self.loggedin = True
                self.client = SteamClientAPI()
                self.SteamGUI.set_client(self.client)
