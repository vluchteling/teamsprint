import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)


def pulse(pin_nr, high_time, low_time):
    GPIO.output(pin_nr, GPIO.HIGH)
    time.sleep(high_time)
    GPIO.output(pin_nr, GPIO.LOW)
    time.sleep(low_time)


def servo_pulse(pin_nr, position):
    a = 0.0005
    b = 0.02
    pulse(pin_nr, (a + (position * (0.002 / 100))), b)


servo = 25
GPIO.setup(servo, GPIO.OUT)

for i in range(0, 50, 1):
    servo_pulse(servo, i)

player = input("welke speller nr kiest u :")

player0 = "offline"
player1 = 'online'
player2 = 'offline'
player3 = "online"

steam_list = [player0, player1, player2, player3]

player = steam_list[int(player)]

GPIO.setup(servo, GPIO.OUT)
if player == 'online':
    for i in range(50, 100, 1):
        servo_pulse(servo, i)
elif player == 'offline':
    for i in range(50, 0, -1):
        servo_pulse(servo, i)
