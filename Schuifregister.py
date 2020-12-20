import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

shift_clock_pin = 5  # deur open doen
latch_clock_pin = 6  # aan doen
data_pin = 13  # informatie

GPIO.setup(shift_clock_pin, GPIO.OUT)
GPIO.setup(latch_clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)


def stopje():
    print("klaar")


def uitklokje(shift_clock_pin, latch_clock_pin, data_pin, delay):
    for g in range(0, 8):
        if g == 0:
            GPIO.output(data_pin, 0)
            GPIO.output(shift_clock_pin, 0)
            GPIO.output(shift_clock_pin, 1)

        else:
            GPIO.output(data_pin, 0)
            GPIO.output(shift_clock_pin, 0)
            GPIO.output(shift_clock_pin, 1)

        GPIO.output(latch_clock_pin, 0)
        GPIO.output(latch_clock_pin, 1)
        time.sleep(delay)
    stopje()


def hc595(shift_clock_pin, latch_clock_pin, data_pin, delay):
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


delay = 1



hc595(shift_clock_pin, latch_clock_pin, data_pin, delay)

uitklokje(shift_clock_pin, latch_clock_pin, data_pin, delay)
