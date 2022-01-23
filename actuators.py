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


lastReadings = 0

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._reg)

class RelayBoard(object):
    __metaclass__ = IterRegistry
    _reg = []

    def __init__(self, device, pin, status):
        self._registry.append(self)
        self.device = device
        self.pin = pin
        self.status = status


ch1 = RelayBoard("valve", 18, false)
ch2 = RelayBoard("nc", 22, false)

ch1_pin = LED(ch1.pin)
ch2_pin = LED(ch2.pin)

# relay board has reversed input, 0 is on...
def activate(device):
    device.off()
    read()

def deactivate(device):
    device.on()
    read()

def setup():
    ch1.on() # inverted!
    ch2.on() # inverted!

def read():

    ch1.status = not ch1_pin.value
    ch2.status = not ch2_pin.value


    send()
    return()

def send():
    try:
        client.connect("192.168.1.100",1883,60)
        for channel in RelayBoard:
            client.publish("growbed1/actuators", json.dumps(channel))
            print(json.dumps(channel))
        client.disconnect()

    except Exception as e:
        print(e)


def set(cmd):
    if cmd['actuator'] == "ch1":
        if cmd['active'] == True:
            activate(valve1)
        elif cmd['active'] == False:
            deactivate(valve1)

    elif cmd['actuator']
