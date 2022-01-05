#!/usr/bin/env python3

"""
Garden automation, subscribing to topics, reading & handling messages.
"""
import time
import paho.mqtt.client as mqtt
client = mqtt.Client("growbed1", False)

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connection Code {0}".format(str(rc)))
    client.subscribe("growbed1/cmd")

def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

def get_commands():
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.connect('192.168.1.100', 1883, 60)
    client.loop_start()
    time.sleep(5)
    client.loop_stop()
