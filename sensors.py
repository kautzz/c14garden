#!/usr/bin/env python3

"""
Garden automation, reading sensors.
"""

import bme680
bme = bme680.BME680()
import paho.mqtt.client as mqtt

def setup_bme():
    bme.set_humidity_oversample(bme680.OS_2X)
    bme.set_pressure_oversample(bme680.OS_4X)
    bme.set_temperature_oversample(bme680.OS_8X)
    bme.set_filter(bme680.FILTER_SIZE_3)
    bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
    bme.set_gas_heater_temperature(320)
    bme.set_gas_heater_duration(150)
    bme.select_gas_heater_profile(0)

def read():
    if bme.get_sensor_data():
        if bme.data.heat_stable:
            readings = {
                "sensor": "BME680",
                "temperature": bme.data.temperature,
                "humidity": bme.data.humidity,
                "pressure": bme.data.pressure,
                "gas_resistance": bme.data.gas_resistance
            }
            send(readings)
            return(readings)
    return(False)

def send(readings):
    client = mqtt.Client()
    client.connect("192.168.1.100",1883,60)
    client.publish("growbed1/sensors", str(readings))
    client.disconnect()
