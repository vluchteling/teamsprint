import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

blue = [8, 0, 0]
green = [0, 255, 0]
red = [0, 0, 255]

clock_pin = 19
data_pin = 26

GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)


def sendsignaal(clock_pin, data_pin, byte):
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


def apa102_send_bytes(clock_pin, data_pin, bytes):
    for p in bytes:
        sendsignaal(clock_pin, data_pin, p)


def apa102(clock_pin, data_pin, colors):
    """
    zend de colors naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin
    
    De colors moet een list zijn, met ieder list element een list van 3 integers,
    in de volgorde [ blauw, groen, rood ].
    Iedere kleur moet in de range 0..255 zijn, 0 voor uit, 255 voor vol aan.
    
    bv: colors = [ [ 0, 0, 0 ], [ 255, 255, 255 ], [ 128, 0, 0 ] ]
    zet de eerste LED uit, de tweede vol aan (wit) en de derde op blauw, halve strekte.
    """
    # apa102_send_bytes(clock_pin, data_pin, blue)
    vierbytes = [0, 0, 0, 0]
    byteMetEnen = [255]
    bytesMetEnen = [255, 255, 255, 255]
    byteToSend = vierbytes + byteMetEnen
    for item in colors:
        byteToSend.extend(item)
    byteToSend.extend(bytesMetEnen)
    apa102_send_bytes(clock_pin, data_pin, byteToSend)


def colors(x, n, on, off):
    result = []
    for i in range(0, n):
        if i == x:
            result.append(on)
        else:
            result.append(off)
    return result


def walk(clock_pin, data_pin, delay, n=8):
    thee = True
    while thee:
        print("u heeft een bericht ")
        for x in range(0, n):
            apa102(clock_pin, data_pin, colors(x, n, red, blue))
            time.sleep(delay)
        for x in range(n - 1, 1, -1):
            apa102(clock_pin, data_pin, colors(x, n, red, blue))
            time.sleep(delay)
        print("Bericht ontvangen ")
        thee = False


walk(clock_pin, data_pin, 0.3)