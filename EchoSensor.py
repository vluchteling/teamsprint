import multiprocessing

import RPi.GPIO as GPIO
import time
import threading


class Sr04:

    def __init__(self):
        self.proc = multiprocessing.Process(target=self.check_status)



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
            print(afstand)

        else:
            print("status afwezig")
            print(afstand)
        time.sleep(1)
        self.check_status()
