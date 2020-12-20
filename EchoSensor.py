import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

gpio20 = 20
gpio21 = 21

GPIO.setup(gpio20, GPIO.OUT)
GPIO.setup(gpio21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def speaker(gpio20, gpio21):
    GPIO.output(gpio20, True)

    time.sleep(0.00001)
    GPIO.output(gpio20, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(gpio21) == False:
        StartTime = time.time()

    while GPIO.input(gpio21) == True:
        StopTime = time.time()

    Time = StopTime - StartTime
    afstand = (Time * 34300) / 2
    if afstand <= 60 or afstand >= 250:
        print(f"{str(afstand)}aanwezig")
    else:
        print(f"{str(afstand)}afwezig")
    # return f'{str(afstand)} druk vingers tegen speaker'


while True:
    same = speaker(gpio20, gpio21)
    time.sleep(60)
