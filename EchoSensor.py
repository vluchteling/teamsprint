import RPi.GPIO as GPIO
import time
import threading


class Sr04(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        check_status()


def check_status():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(0)

    gpio20 = 20
    gpio21 = 21
    GPIO.setup(gpio20, GPIO.OUT)
    GPIO.setup(gpio21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(gpio20, True)
    time.sleep(0.00001)
    GPIO.output(gpio20, False)

    StartTime = time.time()
    StopTime = time.time()
    while not GPIO.input(gpio21):
        StartTime = time.time()
    while GPIO.input(gpio21):
        StopTime = time.time()
    Time = StopTime - StartTime
    afstand = (Time * 34300) / 2
    if afstand <= 80:
        print("status aanwezig")
        print(afstand)

    else:
        print("status afwezig")
        print(afstand)
    time.sleep(1)
    check_status()
