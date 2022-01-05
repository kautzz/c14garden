#!/usr/bin/env python3

"""
Garden automation, system commands.
"""

import os
import sys
import json

def set(cmd):
    if cmd['system'] == "reboot":
        print("Rebooting Now!")
        os.system("reboot")

    elif cmd['system'] == "halt":
        print("Halting Now!")
        os.system("halt")

    elif cmd['system'] == "kill":
        print("Killing Myself!")
        os.system("killall python3")
