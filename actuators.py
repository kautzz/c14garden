#!/usr/bin/env python3

"""
Garden automation, controlling actuators.
"""
from gpiozero import LED
from time import sleep

valve1 = LED(18)

while True:
    led.on()
    sleep(5)
    led.off()
    sleep(5)
