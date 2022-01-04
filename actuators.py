#!/usr/bin/env python3

"""
Garden automation, controlling actuators.
"""
from gpiozero import LED
from time import sleep

valve1 = LED(18)

def set():
    while True:
        valve1.on()
        sleep(5)
        valve1.off()
        sleep(5)
