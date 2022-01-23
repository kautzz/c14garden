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

# class IterRegistry(type):
#     def __iter__(cls):
#         return iter(cls._registry)

class RelayBoard(object):
    #__metaclass__ = IterRegistry
    _registry = []

    def __init__(self, device, pin, status):
        self._registry.append(self)
        self.device = device
        self.gpio = pin
        self.status = status
        _self.pin = LED(pin)

ch1 = RelayBoard("valve", 18, False)
ch2 = RelayBoard("nc", 22, False)

#ch1_pin = LED(ch1.pin)
#ch2_pin = LED(ch2.pin)

# relay board has reversed input, 0 is on...
def activate(device):
    device.off()
    read()

def deactivate(device):
    device.on()
    read()

def setup():
    ch1.pin.on() # inverted!
    ch2.pin.on() # inverted!

def read():

    ch1.status = not ch1.pin.value
    ch2.status = not ch2.pin.value


    send()
    return()

def send():
    try:
        client.connect("192.168.1.100",1883,60)
        for channel in RelayBoard._registry:
            client.publish("growbed1/actuators", json.dumps(channel.__dict__))

            #client.publish("growbed1/actuators", json.dumps(channel))
            print(channel)
        client.disconnect()

    except Exception as e:
        print(e)


def set(cmd):
    # if cmd['actuator'] == "ch1":
    #     if cmd['active'] == True:
    #         activate(valve1)
    #     elif cmd['active'] == False:
    #         deactivate(valve1)
    #
    # elif cmd['actuator']
    pass
