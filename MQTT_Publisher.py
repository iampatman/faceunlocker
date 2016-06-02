from paho.mqtt.client import *


class MQTT_Center:
    def __init__(self, pubid, host):
        self.id = pubid
        self.host = host
        self.client = Mosquitto(client_id= self.id)
        self.client.connect(host=self.host)

    def publish(self, topic, message):
        self.client.publish(topic, message)

