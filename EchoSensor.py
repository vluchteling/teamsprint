import multiprocessing
import time

import RPi.GPIO as GPIO
import gevent


class Sr04:

    def __init__(self, client, neopixel):
        """ init functie van de class"""
        self.proc = multiprocessing.Process(target=self.check_status)
        self.client = client
        self.neopixel = neopixel

    def start(self):
        """ Deze functie start het multiproces"""
        self.proc.start()

    def stop(self):
        """ Deze fucntie stopt het multiproces"""
        # Terminate the process
        self.proc.terminate()  # sends a SIGTERM

    def check_status(self):
        """ Deze functie checkt of er een object binnen 20cm van de sensor is,
        en zet dat vervolgens de status op afwezig."""

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

        trig = 20
        echo = 21
        counter = 0
        terugberichtverstuurd = True
        wegberichtverstuurd = False
        while True:
            try:
                GPIO.setup(trig, GPIO.OUT)
                GPIO.setup(echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.output(trig, True)
                gevent.sleep(0.00001)
                GPIO.output(trig, False)

                StartTime = time.time()
                StopTime = time.time()
                while not GPIO.input(echo):
                    StartTime = time.time()
                while GPIO.input(echo):
                    StopTime = time.time()
                Time = StopTime - StartTime
                afstand = (Time * 34300) / 2
                if afstand >= 20:
                    counter = 0

                    if not terugberichtverstuurd:
                        self.client.change_personastate("aanwezig")
                        self.neopixel.speel_pickup_animatie()
                        terugberichtverstuurd = True
                        wegberichtverstuurd = False
                else:
                    if counter >= 5:

                        if not wegberichtverstuurd:
                            self.client.change_personastate("afwezig")
                            self.neopixel.speel_afk_animatie()
                            wegberichtverstuurd = True
                            terugberichtverstuurd = False
                    counter += 1
                gevent.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                break
