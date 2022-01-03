#!/usr/bin/env python3

"""
Garden automation, main application.
"""

import sensors
import time
import paho.mqtt.client as mqtt


def setup_hardware():
    sensors.setup_bme()

def main():
    setup_hardware()
    try:
        while True:
            print('running main')
            readings = sensors.read_bme()

            if readings:
                print(readings)
                client = mqtt.Client()
                client.connect("192.168.1.100",1883,60)
                client.publish("growbed1/sensors", str(readings))
                client.disconnect()

            time.sleep(10)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
