import RPi.GPIO as GPIO
import time

import gevent

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)


class Servo:

    def pulse(self, pin_nr, high_time, low_time):
        GPIO.output(pin_nr, GPIO.HIGH)
        time.sleep(high_time)
        GPIO.output(pin_nr, GPIO.LOW)
        time.sleep(low_time)

    def servo_pulse(self, pin_nr, position):
        a = 0.0005
        b = 0.02
        self.pulse(pin_nr, (a + (position * (0.002 / 100))), b)

    def start_spel(self, player):
        servo = 25
        GPIO.setup(servo, GPIO.OUT)
        for i in range(0, 50, 1):
            self.servo_pulse(servo, i)

        GPIO.setup(servo, GPIO.OUT)
        gevent.sleep(2)
        if player == 0:
            for i in range(50, 100, 1):
                self.servo_pulse(servo, i)
        else:
            for i in range(50, 0, -1):
                self.servo_pulse(servo, i)

