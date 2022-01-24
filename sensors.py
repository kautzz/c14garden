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

client = mqtt.Client(config['mqtt']['pubcli'], False)

class Sensor(object):
    _registry = []

    def __init__(self):
        self._registry.append(self)
        self.setup()

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
        self.driver = bme680.BME680()
        self.device = device
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.gas_resistance = 0
        super().__init__()


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

class ADS(Sensor):
    def __init__(self, device):
        self.driver = ADS1x15.ADS1115(1)
        self.device = device
        self.battery_voltage = 0
        self.light_intensity = 0
        super().__init__()


    def setup(self):
        self.driver.setGain(0)
        self.driver.setMode(1)
        self.driver.setDataRate(7)

    def read(self):
        self.battery_voltage = round(self.driver.toVoltage(self.driver.readADC_Differential_0_1()) * 2, 2), #multiply by 2 because of voltage divider
        self.light_intensity = round((self.driver.toVoltage(self.driver.readADC_Differential_2_3())) / 0.033, 2) #divide by VCC to get percent

    def tojson(self):
        source = {
            "sensor" : self.device,
            "battery_voltage" : self.device,
            "light_intensity": self.temperature
        }
        return(json.dumps(source))

ads = ADS("ADS1115")

class ISL(Sensor):
    def __init__(self, device):
        self.driver = smbus.SMBus(1)
        self.device = device
        self.green = 0
        self.red = 0
        self.blue = 0
        super().__init__()


    def setup(self):
        # ISL29125 address, 0x44(68)
        # Select configuation-1register, 0x01(01)
        # 0x0D(13) Operation: RGB, Range: 10000 lux, Res: 16 Bits
        self.driver.write_byte_data(0x44, 0x01, 0x0D)

    def read(self):
        # read data from the ISL29125 sensor
        # Read data back from 0x09(9), 6 bytes
        # Green LSB, Green MSB, Red LSB, Red MSB, Blue LSB, Blue MSB
        data = self.driver.read_i2c_block_data(0x44, 0x09, 6)
        green = data[1] * 256 + data[0]
        red = data[3] * 256 + data[2]
        blue = data[5] * 256 + data[4]

        self.green = green
        self.red = red
        self.blue = blue

    def tojson(self):
        source = {
            "sensor" : self.device,
            "light_green" : self.green,
            "light_red": self.red,
            "light_blue": self.blue

        }
        return(json.dumps(source))

isl = ISL("ISL29125")

def read():
    for sensor in Sensor._registry:
        sensor.read()
        sensor.send()
