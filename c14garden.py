#!/usr/bin/env python3

"""
Garden automation, main application.
"""

import sensors
import actuators
import time
import paho.mqtt.client as mqtt


def setup_hardware():
    sensors.setup_bme()

def main():
    setup_hardware()
    try:
        while True:
            print('running main')
            sensReadings = sensors.read()

            if sensReadings:
                client = mqtt.Client()
                client.connect("192.168.1.100",1883,60)
                client.publish("growbed1/sensors", str(sensReadings))
                client.disconnect()

            actReadings = actuators.read()

            client = mqtt.Client()
            client.connect("192.168.1.100",1883,60)
            client.publish("growbed1/actuators", str(actReadings))
            client.disconnect()

            #actuators.toggleloop()
            actuators.valve1.on()
            time.sleep(3)
            actuators.valve1.off()

            time.sleep(10)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
