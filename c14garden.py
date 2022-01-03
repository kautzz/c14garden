#!/usr/bin/env python

"""
Garden automation, main application.
"""

import sensors
import time


def main():
    try:
        while True:
            print('running main')
            readings = sensors.read_bme()
            print(readings)
            time.sleep(10)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
