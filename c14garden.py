#!/usr/bin/env python3

"""
Garden automation, main application.
"""

import sensors
import actuators
import time
import datetime
import paho.mqtt.client as mqtt


def setup_hardware():
    sensors.setup_bme()

def main():
    setup_hardware()
    try:
        while True:
            print(str(datetime.datetime.now()))
            sensReadings = sensors.read()
            actReadings = actuators.read()

            print(str(sensReadings))
            print(str(actReadings))

            time.sleep(5)
            actuators.valve1.on()

            sensReadings = sensors.read()
            actReadings = actuators.read()

            print(str(sensReadings))
            print(str(actReadings))

            time.sleep(5)
            actuators.valve1.off()


    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
