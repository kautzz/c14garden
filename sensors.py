#!/usr/bin/env python3

"""
Garden automation, reading sensors.
"""

#import bme680
#bme = bme680.BME680()
#import ADS1115

import ADS1x15
import RPi.GPIO as GPIO

ads = ADS1x15.ADS1115(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.HIGH)

ads.setInput(0)
ads.setGain(0)
ads.setMode(3)
ads.setDataRate(7)

import paho.mqtt.client as mqtt
import json

from configparser import ConfigParser
config = ConfigParser()
config.read('settings.ini')

#adc = ADS1115.ADS1115()

client = mqtt.Client(config['mqtt']['pubcli'], False)

# def setup_bme():
#     bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
#     bme.set_humidity_oversample(bme680.OS_2X)
#     bme.set_pressure_oversample(bme680.OS_4X)
#     bme.set_temperature_oversample(bme680.OS_8X)
#     bme.set_filter(bme680.FILTER_SIZE_3)
#     bme.set_gas_heater_temperature(320)
#     bme.set_gas_heater_duration(150)
#     bme.select_gas_heater_profile(0)

def read():
    # if bme.get_sensor_data():
    #     readings = {
    #         "sensor": "BME680",
    #         "temperature": bme.data.temperature,
    #         "humidity": bme.data.humidity,
    #         "pressure": bme.data.pressure,
    #     }
    #     if bme.data.heat_stable:
    #         readings['gas_resistance'] = bme.data.gas_resistance

    #a0 = adc.readADCSingleEnded(0, 5160, 250)
    #a1 = adc.readADCSingleEnded(1, 5160, 250)

    value = ads.readADC(0)
    voltage = ads.toVoltage(value)

    diff_value = ads.readADC_Differential_0_1()
    voltage1 = ads.toVoltage(value)

    print(str(ads.getMaxVoltage()))

    readings = {
        "sensor": "ADC",
        "val": diff_value,
        "vol": voltage1
    }

    send(readings)
    return(readings)
    #return()

def send(readings):
    if readings:
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/sensors", json.dumps(readings))
        client.disconnect()
