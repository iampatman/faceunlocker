from paho.mqtt.client import *
import datetime


class MQTT_Center:
    def __init__(self, pubid, host):
        self.id = pubid
        self.host = host
        self.client = Mosquitto(self.id)
        self.client.connect(self.host)

    def publish(self, topic, message):
        self.client.publish(topic, message)

