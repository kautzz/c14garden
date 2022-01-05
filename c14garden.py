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
import json

from configparser import ConfigParser
config = ConfigParser()
config.read('settings.ini')

def setup_hardware():
    sensors.setup_bme()
    actuators.setup_gpio()

def get_readings():
    sensReadings = sensors.read()
    actReadings = actuators.read()
    print(str(datetime.datetime.now()))
    print(json.dumps(sensReadings))
    print(json.dumps(actReadings))
    print("")

def main():
    lastRead = datetime.datetime.now().timestamp() * -1
    setup_hardware()
    try:
        while True:
            if config.getint('intervals', 'readSensorEvery') <= datetime.datetime.now().timestamp() - lastRead:
                get_readings()
                lastRead = datetime.datetime.now().timestamp()

            mqtt_sub.get_commands()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
