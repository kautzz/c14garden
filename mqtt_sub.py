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

client = mqtt.Client(config['device']['name'], False)

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    client.subscribe([
            (config['device']['name'] + "/system/set", 1),
            (config['device']['name'] + "/sensors/set", 1),
            (config['device']['name'] + "/actuators/set", 1)
        ])

def on_message(client, userdata, msg):
    msg_decode=str(msg.payload.decode("utf-8","ignore"))
    try:
        msg_in=json.loads(msg_decode)

        if msg.topic == config['device']['name'] + "/sensors/set":
            pass

        elif msg.topic == config['device']['name'] + "/actuators/set":
            actuators.set(msg_in)

        elif msg.topic == config['device']['name'] + "/system/set":
            systemfcts.set(msg_in)

    except Exception as e:
        print(e)

def get_messages():
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect('192.168.1.100', 1883, 60)
        client.loop_start()
        time.sleep(1)
        client.loop_stop()
    except Exception as e:
        print(e)
