import time

import RPi.GPIO as GPIO

#zorgt er voor dat het kan verbinden #
class Servo:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

    def pulse(self, pin_nr, high_time, low_time):
        GPIO.output(pin_nr, GPIO.HIGH)
        time.sleep(high_time)
        GPIO.output(pin_nr, GPIO.LOW)
        time.sleep(low_time)

    def servo_pulse(self, pin_nr, position):
        #de berekening dat de servo werkt#
        a = 0.0005
        b = 0.02
        self.pulse(pin_nr, (a + (position * (0.002 / 100))), b)

    def start_spel(self, status):
        #de servo wijst naar de status van jouw gekozen vriend #
        servo = 25
        GPIO.setup(servo, GPIO.OUT)
        if status == 0 or status == 7:
            for i in range(50, 100, 1):
                self.servo_pulse(servo, i)
        elif status == 1:
            for i in range(50, 0, -1):
                self.servo_pulse(servo, i)
        else:
            for i in range(0, 50, 1):
                self.servo_pulse(servo, i)
