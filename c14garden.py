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

client = mqtt.Client(config['mqtt']['pubcli'], False)

def setup_hardware():
    sensors.setup()
    actuators.setup()

def get_readings():
    print(str(datetime.datetime.now()))
    print("-----------------------------------------------")
    sensors.read()
    actuators.read()
    print("")

def main():
    lastRead = datetime.datetime.now().timestamp() * -1
    setup_hardware()

    try:
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/system", '{"sysmsg": "script start"}')
        client.disconnect()

    except Exception as e:
        print(e)

    try:
        while True:
            if config.getint('intervals', 'readSensorEvery') <= datetime.datetime.now().timestamp() - lastRead:
                get_readings()
                lastRead = datetime.datetime.now().timestamp()

            mqtt_sub.get_messages()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
