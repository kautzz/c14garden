#!/usr/bin/env python3

"""
Garden automation, system commands.
"""

import os
import sys
import json

def set(cmd):
    if cmd['system'] == "reboot":
        print("rebooting now!")
        os.system("reboot")

    elif cmd['system'] == "halt":
        print("halting now!")
        os.system("halt")

    elif cmd['system'] == "kill":
        print("killing myself!")
        exit()
