import multiprocessing

import RPi.GPIO as GPIO
import time


class Sr04:

    def __init__(self, client):
        self.proc = multiprocessing.Process(target=self.check_status)
        self.client = client

    def start(self):
        self.proc.start()

    def stop(self):
        # Terminate the process
        self.proc.terminate()  # sends a SIGTERM

    def check_status(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

        trig = 20
        echo = 21
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        StartTime = time.time()
        StopTime = time.time()
        while not GPIO.input(echo):
            StartTime = time.time()
        while GPIO.input(echo):
            StopTime = time.time()
        Time = StopTime - StartTime
        afstand = (Time * 34300) / 2
        if afstand <= 80:
            print("status aanwezig")
            self.client.change_status("aanwezig")
            print(afstand)

        else:
            print("status afwezig")
            self.client.change_status("afwezig")
            print(afstand)
        time.sleep(30)
        self.check_status()
