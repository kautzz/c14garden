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

readSensorEvery = 10

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
    lastRead = datetime.datetime.now().timestamp() * -1
    setup_hardware()
    try:
        while True:
            if readSensorEvery <= datetime.timestamp() - lastRead:
                print('Reading Sensors. lastRead: ' + str(lastRead))
                get_readings()
                lastRead = datetime.timestamp()
            else:
                print(str(datetime.timestamp() - lastRead))

            mqtt_sub.get_commands()



    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
