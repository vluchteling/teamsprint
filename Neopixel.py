import atexit
import time

import RPi.GPIO as GPIO


class Neopixel:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)
        atexit.register(self.lights_out)
        self.blue = [8, 0, 0]
        self.green = [0, 255, 0]
        self.red = [0, 0, 255]
        self.yellow = [0, 255, 255]
        self.purple = [255, 0, 255]
        self.off = [0, 0, 0]
        self.clock_pin = 19
        self.data_pin = 26
        self.aantal_lampjes = 8

    def sendsignaal(self, clock_pin, data_pin, byte):
        timeToSleep = 1 / 19000
        byte = ('{:08b}'.format(byte))
        # print(byte)

        for a in byte:
            if int(a) == 0:
                GPIO.output(data_pin, GPIO.LOW)
                # print(0)
            else:
                # print(1)
                GPIO.output(data_pin, GPIO.HIGH)
            GPIO.output(clock_pin, GPIO.HIGH)
            time.sleep(timeToSleep)
            GPIO.output(clock_pin, GPIO.LOW)
            time.sleep(timeToSleep)

    def apa102_send_bytes(self, clock_pin, data_pin, bytes):
        for p in bytes:
            self.sendsignaal(clock_pin, data_pin, p)

    def apa102(self, clock_pin, data_pin, colors):
        """
        zend de colors naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin

        De colors moet een list zijn, met ieder list element een list van 3 integers,
        in de volgorde [ blauw, groen, rood ].
        Iedere kleur moet in de range 0..255 zijn, 0 voor uit, 255 voor vol aan.

        bv: colors = [ [ 0, 0, 0 ], [ 255, 255, 255 ], [ 128, 0, 0 ] ]
        zet de eerste LED uit, de tweede vol aan (wit) en de derde op blauw, halve strekte.
        """
        vierbytes = [0, 0, 0, 0]
        byteMetEnen = [255]
        bytesMetEnen = [255, 255, 255, 255]
        byteToSend = vierbytes
        for item in colors:
            byteToSend.extend(byteMetEnen)
            byteToSend.extend(item)
        byteToSend.extend(bytesMetEnen)
        self.apa102_send_bytes(clock_pin, data_pin, byteToSend)

    def colors(self, x, n, on, off):
        result = []
        for i in range(0, n):
            if i == x:
                result.append(on)
            else:
                result.append(off)
        return result

    def speel_pickup_animatie(self, delay=0):

        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.data_pin, GPIO.OUT)
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.yellow, self.blue))
            time.sleep(delay)
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.off, self.off))

    def speel_afk_animatie(self, delay=0):

        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.data_pin, GPIO.OUT)
        for x in range(self.aantal_lampjes, 0, -1):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.yellow, self.blue))
            time.sleep(delay)
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.off, self.off))

    def speel_loguitanimatie(self, delay=0):

        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.data_pin, GPIO.OUT)
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.green, self.blue))
            time.sleep(delay)
        for x in range(self.aantal_lampjes, 0, -1):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.green, self.blue))
            time.sleep(delay)
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.off, self.off))

    def speel_loginanimatie(self, delay=0):

        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.data_pin, GPIO.OUT)
        for x in range(self.aantal_lampjes, 0, -1):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.purple, self.yellow))
            time.sleep(delay)
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.purple, self.yellow))
            time.sleep(delay)
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.off, self.off))

    def lights_out(self):
        for x in range(0, self.aantal_lampjes):
            self.apa102(self.clock_pin, self.data_pin, self.colors(x, self.aantal_lampjes, self.off, self.off))
