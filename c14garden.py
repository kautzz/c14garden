#!/usr/bin/env python3

"""
Garden automation, main application.
"""

import sensors
import actuators
import mqtt_sub
import time
import datetime
import paho.mqtt.client as mqtt


def setup_hardware():
    sensors.setup_bme()
    actuators.setup_gpio()

def get_readings():
    sensReadings = sensors.read()
    actReadings = actuators.read()
    print(str(datetime.datetime.now()))
    print(str(sensReadings))
    print(str(actReadings))
    print("")

def main():
    setup_hardware()
    try:
        while True:
            get_readings()

            time.sleep(10)



    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
