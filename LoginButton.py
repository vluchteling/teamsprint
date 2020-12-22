import RPi.GPIO as GPIO


class LoginButton:
    def __init__(self):
        self.led = 18
        knopuno = 23
        self.loggedin = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(knopuno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(knopuno, GPIO.RISING, callback=self.login_checker)

    def login_checker(self, mystery_variable):
        if self.loggedin:
            print("u wordt uitgelogd.")
            GPIO.output(self.led, GPIO.LOW)
            self.loggedin = False
        else:
            print("u wordt ingelogd.")
            GPIO.output(self.led, GPIO.HIGH)
            self.loggedin = True
