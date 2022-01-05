#!/usr/bin/env python3

"""
Garden automation, controlling actuators.
"""

from gpiozero import LED
from time import sleep
import paho.mqtt.client as mqtt
import json

from configparser import ConfigParser
config = ConfigParser()
config.read('settings.ini')

client = mqtt.Client(config['mqtt']['pubcli'], False)

# 2 CH relay connected to pin 18 on the pi
valve1 = LED(18)
global lastReadings = 0

# relay board has reversed input, 0 is on...
def activate(device):
    device.off()
    read()

def deactivate(device):
    device.on()
    read()

def setup_gpio():
    deactivate(valve1)

def read():
    readings = {
        "actor": "v1",
        "active": not valve1.value
    }
    send(readings)
    return(readings)

def send(readings):
    global lastReadings
    if readings != lastReadings:
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/actuators", json.dumps(readings))
        client.disconnect()
        lastReadings = readings
    else:
        print("readings did not change")

def set(cmd):
    if cmd['actor'] == "v1":
        if cmd['active'] == True:
            activate(valve1)
        elif cmd['active'] == False:
            deactivate(valve1)
