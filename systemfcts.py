#!/usr/bin/env python3

"""
Garden automation, system commands.
"""

import os
import sys
import json
import paho.mqtt.client as mqtt
client = mqtt.Client(config['mqtt']['pubcli'], False)

def set(cmd):
    if cmd['system'] == "reboot":
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/system", '{"sysmsg": "reboot"}')
        client.disconnect()
        print("Rebooting Now!")
        os.system("sudo reboot")

    elif cmd['system'] == "halt":
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/system", '{"sysmsg": "halt"}')
        client.disconnect()
        print("Halting Now!")
        os.system("sudo halt")

    elif cmd['system'] == "kill":
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/system", '{"sysmsg": "kill"}')
        client.disconnect()
        print("Killing Myself!")
        os.system("killall python3")
