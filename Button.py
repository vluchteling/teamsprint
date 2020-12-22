import RPi.GPIO as GPIO
import time


class Button:
    def __init__(self):
        self.led = 18  # hoeft niet aangesloten te worden heeft geen fuctie
        knopuno = 23
        self.loggedin = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(knopuno, GPIO.RISING, callback=self.login_checker)


    def login_checker(self):
        if self.loggedin:
            print("u wordt uitgelogd.")
            GPIO.output(self.led, GPIO.HIGH)
            self.loggedin = False
        else:
            print("u wordt ingelogd.")
            GPIO.output(self.led, GPIO.LOW)
            self.loggedin = True


"""

while True:
    if GPIO.input(knopuno):
        GPIO.output(led, GPIO.HIGH)
    else:
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.1)"""

