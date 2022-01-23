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
systemcmd = False

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    client.subscribe("growbed1/cmd", 1)

def on_message(client, userdata, msg):
    global systemcmd
    # control actuators remotely
    # {'actuator': 'v1', 'active': True}
    # change settings of individual sensors remotely
    # {'sensor': 'BME680', ...}
    print(client)
    print(userdata)
    print(msg)


    msg_decode=str(msg.payload.decode("utf-8","ignore"))
    print(">>> Command Received", msg_decode)
    try:
        msg_in=json.loads(msg_decode)
        firstKey = list(msg_in.keys())[0]

        if firstKey == 'sensor':
            pass

        elif firstKey == 'system':
            systemcmd = msg_in

        elif firstKey == "actuator":
            actuators.set(msg_in)

        else:
            print("Unknown Command!")

    except Exception as e:
        print("Invalid Message Format!")
        print(e)


def get_commands():
    global systemcmd
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.1.100', 1883, 60)
    client.loop_start()
    #time.sleep(config.getint('intervals', 'readSensorEvery'))
    time.sleep(1)
    client.loop_stop()
    #running sys cmds like kill, reboot, halt after loop_stop so that mqtt message gets consumed
    if systemcmd:
        systemfcts.set(systemcmd)
        systemcmd = False
