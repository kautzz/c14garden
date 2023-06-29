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
import netifaces as ni

from configparser import ConfigParser
config = ConfigParser()
config.read('/home/pi/c14garden/settings.ini')

client = mqtt.Client(config['device']['name'] + "_pub", False)

def get_ip():
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return ip

def get_readings():
    print("------------------------------------------------------")
    print("  ▼▼▼ " + str(datetime.datetime.now()) + " IP: " + str(get_ip()) + " ▼▼▼  ")
    print("------------------------------------------------------")
    sensors.update()
    actuators.update()

def main():
    lastRead = datetime.datetime.now().timestamp() * -1

    try:
        client.connect("192.168.1.100",1883,60)
        client.publish(config['device']['name'] + "/system", '{"sysmsg": "script start", "ip": "' + str(get_ip()) + '", "date": "' + str(datetime.datetime.now()) + '"}', retain=True)
        client.disconnect()

    except Exception as e:
        print(e)

    try:
        while True:
            if config.getint('intervals', 'readSensorEvery') <= datetime.datetime.now().timestamp() - lastRead:
                get_readings()
                actuators.check_schedule()
                lastRead = datetime.datetime.now().timestamp()

            mqtt_sub.get_messages()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
