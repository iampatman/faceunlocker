from paho.mqtt.client import *
import datetime

client = Mosquitto("my_id_pub")
client.connect("localhost")
message = str(datetime.datetime.now())
topic = "tem"
client.publish(topic, message)
