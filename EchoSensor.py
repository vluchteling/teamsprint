import multiprocessing
import RPi.GPIO as GPIO
import time
import gevent


class Sr04:

    def __init__(self, client, gui):
        self.proc = multiprocessing.Process(target=self.check_status)
        self.client = client
        self.gui = gui

    def start(self):
        self.proc.start()

    def stop(self):
        # Terminate the process
        self.proc.terminate()  # sends a SIGTERM

    def check_status(self):
        # self.client.log_in()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(0)

        trig = 20
        echo = 21
        counter = 0
        berichtverstuurd = True
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
            if afstand >= 80:
                counter = 0
                self.client.change_personastate("aanwezig")
                if not berichtverstuurd:
                    #self.gui.stuur_bericht(76561197995118880, "Ik ben weer terug!")
                    berichtverstuurd = True
            else:
                if counter == 10:
                    self.client.change_personastate("afwezig")
                    #self.gui.stuur_bericht(76561197995118880, "Ik ben zo terug.")
                    berichtverstuurd = False
                counter += 1
            gevent.sleep(1)
