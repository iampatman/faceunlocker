import RPi.GPIO as GPIO
import time
import sys


class Sensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN)

    def getState(self):
        return GPIO.input(self.pin)

    def waitFor(self, event):
        GPIO.wait_for_edge(self.pin, event)

    def onStateChange(self, channel):
        sys.exit("should have overriden: onStateChange()")

    def setEvent(self, event):
        GPIO.add_event_detect(self.pin, event, callback=self.onStateChange)