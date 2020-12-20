import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

led = 7  # hoeft niet aangesloten te worden heeft geen fuctie
knopuno = 23
loggedin = False


def login_checker():
    if loggedin:
        print("u bent uitgelogd")
    else:
        print("U bent ingelogd")


GPIO.setup(led, GPIO.OUT)
GPIO.setup(knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.RISING, callback=login_checker())

