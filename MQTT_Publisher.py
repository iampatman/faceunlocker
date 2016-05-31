from paho.mqtt.client import *
from paho.mqtt.publish import *
import datetime

client = Mosquitto("my_id_pub")
client.connect("localhost")
message = str(datetime.datetime.now())
topic = "temp1"
client.publish(topic, message)
