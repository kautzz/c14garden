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

class RelayBoard(object):
    #__metaclass__ = IterRegistry
    _registry = []

    def __init__(self, device, pin, inverted):
        self._registry.append(self)
        self._pin = LED(pin)
        self.device = device
        self.gpio = pin
        self.inverted = inverted
        self.status = False

    def activate(self):
        if self.inverted: self._pin.off()
        else: self._pin.on()

    def deactivate(self):
        if self.inverted: self._pin.on()
        else: self._pin.off()

    def read(self):
        if self.inverted: self.status = not self._pin.value
        else: self.status = self._pin.value

ch1 = RelayBoard("valve", 18, True)
ch2 = RelayBoard("nc", 22, True)


def setup():
    ch1.deactivate()
    ch2.deactivate()

def read():

    ch1.read()
    ch2.read()

    send()
    return()

def send():
    try:
        client.connect("192.168.1.100",1883,60)
        for channel in RelayBoard._registry:
            client.publish("growbed1/actuators", json.dumps(vars(channel)))

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
