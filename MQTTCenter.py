from paho.mqtt.client import *
from threading import *
import hashlib


class MQTTCenter:
    def __init__(self, pubid, host, lcd=None, relay=None):
        self.id = pubid
        self.host = host
        self.client = Mosquitto(client_id=self.id)
        self.client.connect(host=self.host)
        self.time = time.time()
        self.client.on_message = self.on_message
        self.client.subscribe("trung1")
        self.currentKey = ""
        self.open = False
        self.lcd = lcd
        self.relay = relay
        self.timer = Timer(30, self.stoplistening)

    def publish(self, topic, message):
        self.time = time.time()
        sig = hashlib.sha1(message + "abc@123").hexdigest().upper()
        self.currentKey = sig
        data = message + "|" + sig
        print ("Message published: %s" % data)
        self.client.publish(topic, data, qos=1)
        self.timer = Timer(30, self.stoplistening)
        self.timer.start()

    def stoplistening(self):
        print ("Stop listening canceled by timer")
        self.currentKey = ""

    def opendoor(self):
	self.lcd.clear()
        self.lcd.display_string(line=0, string="Welcome home")
        self.relay.switchall(int(1))
        time.sleep(5)
        self.relay.switchall(int(0))

    def denyopeningdoor(self, message):
	self.lcd.clear()
        self.lcd.display_string(line=0, string=message)
	time.sleep(5)

    def on_message(self, c, userdata, mesg):
        print "message: %s %s %s" % (userdata, mesg.topic, mesg.payload)
        payload = str(mesg.payload)
        param = payload.split("|")
        self.timer.cancel()
        currentTime = time.time()
        difTime = currentTime - self.time
        if difTime < 30:
            if len(param) == 3 and param[2] == self.currentKey:
                self.open = (param[0] == "Accept")
        self.currentKey = ""
        if self.open:
            print ("open")
            self.opendoor()
        else:
            print ("deny")
            self.denyopeningdoor(param[1])


def main():
    mqtt = MQTTCenter(pubid="id", host="dkiong.no-ip.biz")
    while True:
        mqtt.client.loop(timeout=1000)
        print("hi")


if __name__ == '__main__':
    main()
