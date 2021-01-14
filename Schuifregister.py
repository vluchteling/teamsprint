import time

import RPi.GPIO as GPIO


class Schuifregister:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

        shift_clock_pin = 5
        latch_clock_pin = 6
        data_pin = 13
        delay = 0.1

        GPIO.setup(shift_clock_pin, GPIO.OUT)
        GPIO.setup(latch_clock_pin, GPIO.OUT)
        GPIO.setup(data_pin, GPIO.OUT)

    def hc595(self, shift_clock_pin, latch_clock_pin, data_pin, value, delay):
        if value % 2 == 1:
            GPIO.output(data_pin, 1)
            GPIO.output(shift_clock_pin, 0)
            GPIO.output(shift_clock_pin, 1)
            GPIO.output(latch_clock_pin, 0)
            GPIO.output(latch_clock_pin, 1)
            time.sleep(delay)
        else:
            GPIO.output(data_pin, 0)
            GPIO.output(shift_clock_pin, 0)
            GPIO.output(shift_clock_pin, 1)
            GPIO.output(latch_clock_pin, 0)
            GPIO.output(latch_clock_pin, 1)
            time.sleep(delay)

    def lichtjes(self, aantal):
        cijfer = aantal
        shift_clock_pin = 5
        latch_clock_pin = 6
        data_pin = 13
        delay = 0.1

        # Resets the all the leds
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)
        self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)

        if cijfer == 0:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 0, delay)

        elif cijfer == 1:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)

        elif cijfer == 2:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)

        elif cijfer == 3:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)

        elif cijfer == 4:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)

        elif cijfer == 5:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)

        elif cijfer == 6:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)

        elif cijfer == 7:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)

        elif cijfer >= 8:
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
            self.hc595(shift_clock_pin, latch_clock_pin, data_pin, 1, delay)
