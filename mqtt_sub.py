#!/usr/bin/env python3

"""
Garden automation, subscribing to topics, reading & handling messages.
"""
import time
import json
import paho.mqtt.client as mqtt
import actuators

from configparser import ConfigParser
config = ConfigParser()
config.read('settings.ini')

client = mqtt.Client(config['mqtt']['subcli'], False)

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    client.subscribe("growbed1/cmd", 1)

def on_message(client, userdata, msg):
    # control actuators remotely
    # {'actor': 'v1', 'active': True}
    # change settings of individual sensors remotely
    # {'sensor': 'BME680', ...}

    msg_decode=str(msg.payload.decode("utf-8","ignore"))
    print("Data Received", msg_decode)
    try:
        msg_in=json.loads(msg_decode)
        firstKey = list(msg_in.keys())[0]
        print(firstKey)

        if firstKey == "actor":
            print("actuator key detected")
            actuators.set(msg_in)

        elif firstKey == 'sensor':
            pass

        else:
            print("No Sensor Or Actuator Specified!")

    except Exception as e:
        print("Invalid Message Format!")
        print(e)


def get_commands():
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.connect('192.168.1.100', 1883, 60)
    client.loop_start()
    time.sleep(config.getint('intervals', 'readSensorEvery'))
    client.loop_stop()
