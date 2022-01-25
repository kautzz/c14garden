#!/usr/bin/env python3

"""
Garden automation, controlling actuators.
"""

from gpiozero import LED
from time import sleep
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('settings.ini')

client = mqtt.Client(config['mqtt']['pubcli'], False)

class RelayBoard(object):
    _registry = []

    def __init__(self, device, pin, inverted):
        self._registry.append(self)
        self._pin = LED(pin)
        self.device = device
        self.schedule = json.loads(config['schedule'][device])
        self.gpio = pin
        self.inverted = inverted
        self.status = False
        self.last_status = False
        self.deactivate()


    def activate(self):
        if self.inverted: self._pin.off()
        else: self._pin.on()
        self.last_status = self.status
        self.read()
        self.send()

    def deactivate(self):
        if self.inverted: self._pin.on()
        else: self._pin.off()
        self.last_status = self.status
        self.read()
        self.send()

    def check_schedule(self):
        day = datetime.today().strftime('%A')
        print(day)
        for interval in self.schedule:
            if interval.list(message.keys())[0] == day:
                print("matching day")

    def read(self):
        if self.inverted: self.status = not self._pin.value
        else: self.status = self._pin.value

    def tojson(self):
        source = {
            self.device : self.status,
            "gpio": self.gpio,
            "inv": self.inverted,
            "schedule": self.schedule
        }
        return(json.dumps(source))

    def send(self):
        if self.last_status != self.status:
            try:
                client.connect("192.168.1.100",1883,60)
                client.publish("growbed1/actuators", self.tojson())
                client.disconnect()

            except Exception as e:
                print(e)

            self.last_status = self.status
        print(self.tojson())


    def set(self, status):
        if status == True:
            self.activate()
        elif status == False:
            self.deactivate()

ch1 = RelayBoard("valve", 18, True)
ch2 = RelayBoard("nc", 23, True)

def update():
    for channel in RelayBoard._registry:
        channel.read()
        channel.send()

def set(message):
    for channel in RelayBoard._registry:
        key = list(message.keys())[0]

        if key == channel.device and message[key] == "schedule":
            if message["duration"] and message["amount"]:
                del message[key]
                channel.schedule.append(message)
                config['schedule'][channel.device] = json.dumps(channel.schedule)
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                channel.last_status = 0
                print("▶ Added interval to " + key + " schedule")

        elif key == channel.device and message[key] == "deschedule":
            day = list(message.keys())[1]
            for interval in channel.schedule:
                if (day == list(interval.keys())[0]
                    and message["duration"] == interval["duration"]
                    and message["amount"] == interval["amount"]):

                    channel.schedule.remove(interval)
                    config['schedule'][channel.device] = json.dumps(channel.schedule)
                    with open('settings.ini', 'w') as configfile:
                        config.write(configfile)
                    channel.last_status = 0
                    print("▶ Removed interval from " + key + " schedule")
                    break
                print("▶ Interval does not exist: " + json.dumps(message))

        elif key == channel.device:
            channel.set(message[key])

def check_schedule():
    for channel in RelayBoard._registry:
        channel.check_schedule()
