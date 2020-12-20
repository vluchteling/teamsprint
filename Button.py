import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

led = 7  # hoeft niet aangesloten te worden heeft geen fuctie
knopuno = 23


def jargo():
    print("u bent uitgelogd")


GPIO.setup(led, GPIO.OUT)
GPIO.setup(knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(knopuno):
        GPIO.output(led, GPIO.HIGH)
        jargo()
        time.sleep(0.5)
