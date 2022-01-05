#!/usr/bin/env python3

"""
Garden automation, subscribing to topics, reading & handling messages.
"""
import time
import json
import paho.mqtt.client as mqtt

from configparser import ConfigParser
config = ConfigParser()
config.read('settings.ini')

client = mqtt.Client(config['mqtt']['cli'], False)

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    client.subscribe("growbed1/cmd", 1)

def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

    # control actuators remotely
    # {'actor': 'v1', 'active': True}
    # readings = {
    #     "actor": "v1",
    #     "active": not valve1.value
    # }

    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("data Received type",type(m_decode))
    print("data Received",m_decode)
    print("Converting from Json to Object")
    try:
        m_in=json.loads(m_decode) #decode json data
        print(type(m_in))
        print("broker 2 address = ",m_in["broker2"])
    except:
        print("Invalid Message Format!")

    # change settings of individual sensors remotely
    # {'sensor': 'BME680', ...}


def get_commands():
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.connect('192.168.1.100', 1883, 60)
    client.loop_start()
    time.sleep(config.getint('intervals', 'readSensorEvery'))
    client.loop_stop()
