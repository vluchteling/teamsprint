import atexit
import time

import RPi.GPIO as GPIO


class LoginButton:
    def __init__(self, steamgui):
        """ init functie van de class"""
        self.SteamGUI = steamgui
        self.led = 18
        self.knopuno = 23
        self.loggedin = True
        self.keep_running = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(self.knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.knopuno, GPIO.BOTH, callback=self.login_checker)
        GPIO.output(self.led, GPIO.HIGH)
        atexit.register(self.lights_out)

    def login_checker(self, twentythree):
        """ Deze functie geeft een callback aan SteamGUI als er op de knop wordt gedrukt"""

        if not GPIO.input(self.knopuno):

            if self.loggedin:
                GPIO.output(self.led, GPIO.LOW)
                self.loggedin = False
                self.SteamGUI.log_out()

            else:
                GPIO.output(self.led, GPIO.HIGH)
                self.loggedin = True
                self.SteamGUI.log_in()
        time.sleep(1)

    def lights_out(self):
        """ Deze functie zet het lampje uit"""
        self.keep_running = False
        GPIO.remove_event_detect(self.knopuno)
        GPIO.output(self.led, GPIO.LOW)

