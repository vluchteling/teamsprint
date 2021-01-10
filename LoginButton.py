import atexit
import RPi.GPIO as GPIO


class LoginButton:
    def __init__(self, steamgui):
        self.SteamGUI = steamgui
        self.led = 18
        self.knopuno = 23
        self.loggedin = True
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

                print("u wordt uitgelogd.")
                GPIO.output(self.led, GPIO.LOW)
                self.loggedin = False
                self.SteamGUI.log_out()

            else:
                print("u wordt ingelogd.")
                GPIO.output(self.led, GPIO.HIGH)
                self.loggedin = True
                self.SteamGUI.log_in()
        # gevent.sleep(1)

    def lights_out(self):
        GPIO.output(self.led, GPIO.LOW)
