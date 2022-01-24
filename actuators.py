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
        self.read()

    def deactivate(self):
        if self.inverted: self._pin.on()
        else: self._pin.off()
        self.read()

    def read(self):
        if self.inverted: self.status = not self._pin.value
        else: self.status = self._pin.value

    def tojson(self):
        source = {
            self.device : self.status,
            "gpio": self.gpio,
            "inv": self.inverted,
        }
        return(json.dumps(source))

    def send(self):
        try:
            client.connect("192.168.1.100",1883,60)
            client.publish("growbed1/actuators", self.tojson())
            print(self.tojson())
            client.disconnect()

        except Exception as e:
            print(e)

    def set(self, status):
        if status == True:
            self.activate()
        elif status == False:
            self.deactivate()
        self.send()

ch1 = RelayBoard("valve", 18, True)
ch2 = RelayBoard("nc", 22, True)

def setup():
    for channel in RelayBoard._registry:
        channel.deactivate()

def read():
    for channel in RelayBoard._registry:
        channel.read()
    send()

def send():
    for channel in RelayBoard._registry:
        channel.send()

def set(message):
    for channel in RelayBoard._registry:
        if channel.device == list(message.keys())[0]:
            channel.set(list(message.keys())[1])

    # if cmd['actuator'] == "ch1":
    #     if cmd['active'] == True:
    #         activate(valve1)
    #     elif cmd['active'] == False:
    #         deactivate(valve1)
    #
    # elif cmd['actuator']
    pass
