#!/usr/bin/env python3

"""
Garden automation, controlling actuators.
"""
from gpiozero import LED
from time import sleep
import paho.mqtt.client as mqtt

valve1 = LED(18)

def setup_gpio():
    valve1.off()

def read():
    readings = {
        "actor": "v1",
        "active": not valve1.value
    }
    send(readings)
    return(readings)

def send(readings):
    if readings:
        client = mqtt.Client()
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/actuators", str(readings))
        client.disconnect()

def toggleloop():
    while True:
        valve1.on()
        sleep(5)
        valve1.off()
        sleep(5)
