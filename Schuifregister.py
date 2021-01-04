import RPi.GPIO as GPIO
import time


class Schuifregister:

    def __init__(self):
        delay = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

        self.shift_clock_pin = 5  # deur open doen
        self.latch_clock_pin = 6  # aan doen
        self.data_pin = 13  # informatie

        GPIO.setup(self.shift_clock_pin, GPIO.OUT)
        GPIO.setup(self.latch_clock_pin, GPIO.OUT)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

        self.hc595(self.shift_clock_pin, self.latch_clock_pin, self.data_pin, delay)

        self.uitklokje(self.shift_clock_pin, self.latch_clock_pin, self.data_pin, delay)

    def stopje(self):
        print("klaar")

    def uitklokje(self, shift_clock_pin, latch_clock_pin, data_pin, delay):
        for g in range(0, 8):
            if g == 0:
                GPIO.output(self.data_pin, 0)
                GPIO.output(self.shift_clock_pin, 0)
                GPIO.output(self.shift_clock_pin, 1)

            else:
                GPIO.output(self.data_pin, 0)
                GPIO.output(self.shift_clock_pin, 0)
                GPIO.output(self.shift_clock_pin, 1)

            GPIO.output(latch_clock_pin, 0)
            GPIO.output(latch_clock_pin, 1)
            time.sleep(delay)
        self.stopje()

    def hc595(self, shift_clock_pin, latch_clock_pin, data_pin, delay):
        for g in range(0, 8):
            if g == 0:
                GPIO.output(data_pin, 1)
                GPIO.output(shift_clock_pin, 0)
                GPIO.output(shift_clock_pin, 1)

            else:
                GPIO.output(data_pin, 0)
                GPIO.output(shift_clock_pin, 0)
                GPIO.output(shift_clock_pin, 1)

            GPIO.output(latch_clock_pin, 0)
            GPIO.output(latch_clock_pin, 1)
            time.sleep(1)
