#!/usr/bin/env python3

"""
Garden automation, system commands.
"""

import os
import sys
import json
import paho.mqtt.client as mqtt

from configparser import ConfigParser
config = ConfigParser()
config.read('/home/pi/c14garden/settings.ini')

client = mqtt.Client(config['device']['name'] + "_pub", False)

def set(cmd):
    if cmd['system'] == "reboot":
        client.connect("192.168.1.100",1883,60)
        client.publish(config['device']['name'] + "/system", '{"sysmsg": "reboot"}')
        client.disconnect()
        print("Rebooting Now!")
        os.system("sleep 3 && sudo reboot &")

    elif cmd['system'] == "halt":
        client.connect("192.168.1.100",1883,60)
        client.publish(config['device']['name'] + "/system", '{"sysmsg": "halt"}')
        client.disconnect()
        print("Halting Now!")
        os.system("sleep 3 && sudo halt &")

    if cmd['system'] == "kill":
        client.connect("192.168.1.100",1883,60)
        client.publish(config['device']['name'] + "/system", '{"sysmsg": "kill"}')
        client.disconnect()
        print("Killing Myself!")
        os.system("sleep 3 && killall python3 &")
