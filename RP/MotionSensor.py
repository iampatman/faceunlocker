import time
from Sensor import *


class MotionSensor(Sensor):
    def __init__(self, pin):
        Sensor.__init__(self, pin)

    def onStateChange(self, channel):
        print "%s: pin: %d state: %d" % (time.asctime(), channel, self.getState())

def main():
    sensor = MotionSensor(17)
    sensor.setEvent(GPIO.BOTH)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
