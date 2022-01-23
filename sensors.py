#!/usr/bin/env python3

"""
Garden automation, reading sensors.
"""

import bme680
import ADS1x15
import smbus
import paho.mqtt.client as mqtt
import json
from configparser import ConfigParser

bme = bme680.BME680()
ads = ADS1x15.ADS1115(1)

ads.setGain(0)
ads.setMode(1)
ads.setDataRate(7)

config = ConfigParser()
config.read('settings.ini')

client = mqtt.Client(config['mqtt']['pubcli'], False)


def setup_isl():
    # Get I2C bus
    bus = smbus.SMBus(1)

    # ISL29125 address, 0x44(68)
    # Select configuation-1register, 0x01(01)
    # 0x0D(13) Operation: RGB, Range: 10000 lux, Res: 16 Bits
    bus.write_byte_data(0x44, 0x01, 0x0D)

def setup_bme():
    bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
    bme.set_humidity_oversample(bme680.OS_2X)
    bme.set_pressure_oversample(bme680.OS_4X)
    bme.set_temperature_oversample(bme680.OS_8X)
    bme.set_filter(bme680.FILTER_SIZE_3)
    bme.set_gas_heater_temperature(320)
    bme.set_gas_heater_duration(150)
    bme.select_gas_heater_profile(0)

def read():

    # read and send data from BME senor
    if bme.get_sensor_data():
        bme_readings = {
            "sensor": "BME680",
            "temperature": round(bme.data.temperature, 2),
            "humidity": round(bme.data.humidity, 2),
            "pressure": round(bme.data.pressure, 2)
        }
        if bme.data.heat_stable:
            bme_readings['gas_resistance'] = round(bme.data.gas_resistance)

        send(bme_readings)

    # read and send data from ADC
    batt_readings = {
        "sensor": "ADS1115",
        "battery_voltage": round(ads.toVoltage(ads.readADC_Differential_0_1()) * 2, 2), #multiply by 2 because of voltage divider
        "light_intensity": round((ads.toVoltage(ads.readADC_Differential_2_3())) / 0.033, 2) #divide by VCC to get percent
    }

    send(batt_readings)

    # read and send data from the ISL29125 sensor

    # ISL29125 address, 0x44(68)
    # Read data back from 0x09(9), 6 bytes
    # Green LSB, Green MSB, Red LSB, Red MSB, Blue LSB, Blue MSB
    data = bus.read_i2c_block_data(0x44, 0x09, 6)
    green = data[1] * 256 + data[0]
    red = data[3] * 256 + data[2]
    blue = data[5] * 256 + data[4]

    isl_readings = {
        "sensor": "ISL29125",
        "green": green,
        "red": red,
        "blue": blue
    }

    # Output data to the screen
    print "Green Color luminance : %d lux" %green
    print "Red Color luminance : %d lux" %red
    print "Blue Color luminance : %d lux" %blue

    send(isl_readings)

    return()

def send(readings):
    if readings:
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/sensors", json.dumps(readings))
        client.disconnect()
        print(json.dumps(readings))
