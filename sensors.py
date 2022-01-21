#!/usr/bin/env python3

"""
Garden automation, reading sensors.
"""

#import bme680
#bme = bme680.BME680()

import ADS1x15
ads = ADS1x15.ADS1115(1)

#ads.setInput(0)
ads.setGain(0)
#ads.setMode(1)
#ads.setDataRate(7)

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
    print("Gain before read: " + str(ads.getGain()))

    diff_adc_1 = ads.readADC_Differential_0_1()
    battery_voltage = ads.toVoltage(diff_adc_1)

    diff_adc_2 = ads.readADC_Differential_2_3()
    light_intensity = ads.toVoltage(diff_adc_2)

    print("Gain after read: " + str(ads.getGain()))


    readings = {
        "sensor": "ADS1115",
        "raw_adc_1": diff_adc_1,
        "raw_adc_2": diff_adc_2,
        "battery_voltage": battery_voltage,
        "light_intensity": light_intensity

    }

    send(readings)
    return(readings)
    #return()

def send(readings):
    if readings:
        client.connect("192.168.1.100",1883,60)
        client.publish("growbed1/sensors", json.dumps(readings))
        client.disconnect()
