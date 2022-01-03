#!/usr/bin/env python

"""
Garden automation, reading bmes.
"""

import bme680
bme = bme680.BME680()

def setup_bme():
    print('setting up bme')
    bme.set_humidity_oversample(bme680.OS_2X)
    bme.set_pressure_oversample(bme680.OS_4X)
    bme.set_temperature_oversample(bme680.OS_8X)
    bme.set_filter(bme680.FILTER_SIZE_3)
    bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
    bme.set_gas_heater_temperature(320)
    bme.set_gas_heater_duration(150)
    bme.select_gas_heater_profile(0)

def read_bme():
    print('reading bme data')
    if bme.get_sensor_data():
        if bme.data.heat_stable:
            print('heat stable!')

        #output = "{0:.2f} C, {1:.2f} hPa, {2:.2f} %RH, {3:.2f} ohm".format(bme.data.temperature, bme.data.pressure, bme.data.humidity, bme.data.gas_resistance)
        readings = {
            "temperature": bme.data.temperature,
            "humidity": bme.data.humidity,
            "pressure": bme.data.pressure,
            "gas_resistance": bme.data.gas_resistance
        }
        return(readings)
