import time

import RPi.GPIO as GPIO

from SteamClientAPI import SteamClientAPI


class LoginButton:
    def __init__(self):
        self.led = 18
        self.knopuno = 23
        self.loggedin = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(self.knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.knopuno, GPIO.RISING, callback=self.login_checker)
        GPIO.output(self.led, GPIO.LOW)

    def login_checker(self, mystery_variable):
        print(mystery_variable)
        if GPIO.input(self.knopuno):
            if self.loggedin:
                print("u wordt uitgelogd.")
                GPIO.output(self.led, GPIO.LOW)
                self.loggedin = False
                self.client.log_out()
                # time.sleep(1)

            else:
                print("u wordt ingelogd.")
                GPIO.output(self.led, GPIO.HIGH)
                self.loggedin = True
                self.client = SteamClientAPI()
                # time.sleep(1)
