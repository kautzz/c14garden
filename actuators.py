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

# relay board has reversed input, 0 is on...
def activate(device):
    device.off()

def deactivate(device):
    device.on()

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
    if readings:
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/actuators", json.dumps(readings))
        client.disconnect()

def set(cmd):
    print(cmd)
    device = cmd['actor']
    status = cmd['active']

    read()

def toggleloop():
    while True:
        valve1.on()
        sleep(5)
        valve1.off()
        sleep(5)
