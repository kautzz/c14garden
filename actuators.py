#!/usr/bin/env python3

"""
Garden automation, controlling actuators.
"""

from gpiozero import LED
from time import sleep
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('settings.ini')

client = mqtt.Client(config['device']['name'] + "_pub", False)

class RelayBoard(object):
    _registry = []

    def __init__(self, device, pin, inverted):
        self._registry.append(self)
        self._pin = LED(pin)
        self.device = device
        self.schedule = json.loads(config['schedule'][device])
        self.schedule_active = False
        self.schedule_start = datetime.today()
        self.gpio = pin
        self.inverted = inverted
        self.status = False
        self.last_status = False
        self.deactivate()

    def activate(self):
        if self.inverted: self._pin.off()
        else: self._pin.on()
        self.last_status = self.status
        self.schedule_active = False
        self.read()
        self.send()

    def deactivate(self):
        if self.inverted: self._pin.on()
        else: self._pin.off()
        self.last_status = self.status
        self.schedule_active = False
        self.read()
        self.send()

    def check_schedule(self):
        day = datetime.today().strftime('%A').lower()
        time = datetime.today().strftime('%H:%M')
        for interval in self.schedule:

            if (list(interval.keys())[0] == day
                and interval[day] == time
                and self.schedule_active == False):
                self.schedule_start = datetime.today()
                self.activate()
                self.schedule_active = True

            elif (list(interval.keys())[0] == day
                and self.schedule_start.strftime('%H:%M') == interval[day]
                and self.schedule_start + timedelta(minutes=interval["duration"]) <= datetime.today()
                and self.schedule_active == True):
                self.deactivate()

            elif self.schedule_start.strftime('%H:%M') == interval[day]:
                print(str(self.schedule_start))
                print(str(self.schedule_start + timedelta(minutes=interval["duration"])))
                print(str(datetime.today()))

            print(self.schedule_active)

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
                client.publish(config['device']['name'] + "/actuators", self.tojson())
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
                channel.last_status = not channel.last_status
                print("▶▶▶ Added interval to " + key + " schedule")
                channel.send()

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
                    channel.last_status = not channel.last_status
                    print("▶▶▶ Removed interval from " + key + " schedule")
                    channel.send()
                print("▶▶▶ Interval does not exist: " + json.dumps(message))

        elif key == channel.device and message[key] == "deschedule_all":
            channel.schedule.clear()
            config['schedule'][channel.device] = "[]"
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            channel.last_status = not channel.last_status
            print("▶▶▶ Removed all intervals from " + key + " schedule")
            channel.send()

        elif key == channel.device:
            channel.set(message[key])

def check_schedule():
    for channel in RelayBoard._registry:
        channel.check_schedule()
