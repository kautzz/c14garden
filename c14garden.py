"""
Garden automation, main application.
"""

import sensors

def main():
    print('running main')
    sensors.read_bme()

if __name__ == "__main__":
    main()

print('')
print('[ ☑ End Of Program ]')
