#!/usr/bin/env python3

"""
Garden automation, subscribing to topics, reading & handling messages.
"""
import time
import json
import paho.mqtt.client as mqtt
import actuators
import systemfcts

from configparser import ConfigParser
config = ConfigParser()
config.read('settings.ini')

client = mqtt.Client(config['mqtt']['subcli'], False)

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    client.subscribe([
            ("growbed1/system/set", 1),
            ("growbed1/sensor/set", 1),
            ("growbed1/actuator/set", 1)
        ])

def on_message(client, userdata, msg):
    global systemcmd
    # control actuators remotely
    # {'actuator': 'v1', 'active': True}
    # change settings of individual sensors remotely
    # {'sensor': 'BME680', ...}

    msg_decode=str(msg.payload.decode("utf-8","ignore"))
    try:
        msg_in=json.loads(msg_decode)

        if msg.topic == 'growbed1/sensor/set':
            pass

        elif msg.topic == 'growbed1/actuator/set':
            actuators.set(msg_in)

        elif msg.topic == "growbed1/system/set":
            pass

    except Exception as e:
        print("Invalid Message Format!")
        print(e)


def get_messages():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.1.100', 1883, 60)
    client.loop_start()
    time.sleep(1)
    client.loop_stop()
