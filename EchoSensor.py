import multiprocessing
import RPi.GPIO as GPIO
import time
import gevent
from Berichtverstuurder import Berichtverstuurder


class Sr04:

    def __init__(self, client, gui, vriend):
        self.proc = multiprocessing.Process(target=self.check_status)
        self.client = client
        self.gui = gui
        self.vriend = vriend
        if self.vriend == "begin":
            self.vriend = None

    def start(self):
        self.proc.start()

    def stop(self):
        # Terminate the process
        self.proc.terminate()  # sends a SIGTERM


    def check_status(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

        trig = 20
        echo = 21
        counter = 0
        terugberichtverstuurd = True
        wegberichtverstuurd = False
        while True:
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
                self.client.change_personastate("aanwezig")
                if not terugberichtverstuurd:
                    if self.vriend is not None:
                        self.gui.stuur_bericht(self.vriend,"Ik ben weer terug!")
                        terugberichtverstuurd = True
                        wegberichtverstuurd = False
            else:
                if counter >= 5:
                    self.client.change_personastate("afwezig")
                    if self.vriend is not None and not wegberichtverstuurd:
                        self.gui.stuur_bericht(self.vriend,"Ik ben zo terug.")
                        wegberichtverstuurd = True
                        terugberichtverstuurd = False
                counter += 1
            gevent.sleep(1)
