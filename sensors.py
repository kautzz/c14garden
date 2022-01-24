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

config = ConfigParser()
config.read('settings.ini')

isl = smbus.SMBus(1)
ads = ADS1x15.ADS1115(1)

client = mqtt.Client(config['mqtt']['pubcli'], False)

class Sensor(object):
    _registry = []

    def __init__(self):
        self._registry.append(self)

    def send(self):
        try:
            client.connect("192.168.1.100",1883,60)
            client.publish("growbed1/sensors", self.tojson())
            print(self.tojson())
            client.disconnect()

        except Exception as e:
            print(e)

class BME(Sensor):
    def __init__(self, device):
        super().__init__()
        self.driver = bme680.BME680()
        self.device = device
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.gas_resistance = 0

    def setup(self):
        self.driver.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.driver.set_humidity_oversample(bme680.OS_2X)
        self.driver.set_pressure_oversample(bme680.OS_4X)
        self.driver.set_temperature_oversample(bme680.OS_8X)
        self.driver.set_filter(bme680.FILTER_SIZE_3)
        self.driver.set_gas_heater_temperature(320)
        self.driver.set_gas_heater_duration(150)
        self.driver.select_gas_heater_profile(0)

    def read(self):
        if self.driver.get_sensor_data():
            self.temperature = round(self.driver.data.temperature, 2)
            self.humidity = round(self.driver.data.humidity, 2)
            self.pressure = round(self.driver.data.pressure, 2)
            self.gas_resistance = round(self.driver.data.gas_resistance)

    def tojson(self):
        source = {
            "sensor" : self.device,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "gas_resistance": self.gas_resistance
        }
        return(json.dumps(source))

bme = BME("BME680")


def setup():
    pass

def read():
    for sensor in Sensors._registry:
        sensor.read()
        sensor.send()

#
# def setup():
#     setup_ads()
#     setup_isl()
#
# def setup_ads():
#     ads.setGain(0)
#     ads.setMode(1)
#     ads.setDataRate(7)
#
# def setup_isl():
#     # ISL29125 address, 0x44(68)
#     # Select configuation-1register, 0x01(01)
#     # 0x0D(13) Operation: RGB, Range: 10000 lux, Res: 16 Bits
#     isl.write_byte_data(0x44, 0x01, 0x0D)
#
#
# def read():
#
#     # read data from BME senor
#     if bme.get_sensor_data():
#         bme_readings = {
#             "sensor": "BME680",
#             "temperature": round(bme.data.temperature, 2),
#             "humidity": round(bme.data.humidity, 2),
#             "pressure": round(bme.data.pressure, 2)
#         }
#         if bme.data.heat_stable:
#             bme_readings['gas_resistance'] = round(bme.data.gas_resistance)
#         send(bme_readings)
#
#     # read data from ADC
#     batt_readings = {
#         "sensor": "ADS1115",
#         "battery_voltage": round(ads.toVoltage(ads.readADC_Differential_0_1()) * 2, 2), #multiply by 2 because of voltage divider
#         "light_intensity": round((ads.toVoltage(ads.readADC_Differential_2_3())) / 0.033, 2) #divide by VCC to get percent
#     }
#     send(batt_readings)
#
#     # read data from the ISL29125 sensor
#     # Read data back from 0x09(9), 6 bytes
#     # Green LSB, Green MSB, Red LSB, Red MSB, Blue LSB, Blue MSB
#     data = isl.read_i2c_block_data(0x44, 0x09, 6)
#     green = data[1] * 256 + data[0]
#     red = data[3] * 256 + data[2]
#     blue = data[5] * 256 + data[4]
#
#     isl_readings = {
#         "sensor": "ISL29125",
#         "light_green": green,
#         "light_red": red,
#         "light_blue": blue
#     }
#     send(isl_readings)
#
#     return()
#
# def send(readings):
#     try:
#         client.connect("192.168.1.100",1883,60)
#         client.publish("growbed1/sensors", json.dumps(readings))
#         client.disconnect()
#         print(json.dumps(readings))
#     except Exception as e:
#         print(e)
