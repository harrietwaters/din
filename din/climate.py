import json
import time
import Adafruit_DHT

class ClimateSensor():
    sensor = None
    pin = None

    def __init__ (self):
        self.sensor = Adafruit_DHT.DHT11
        self.pin = 4


    def get_climate(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        if humidity is not None and temperature is not None:
            return {
                'temperature': '{0:0.1f}'.format(self.celsiusToFahrenheit(temperature)),
                'humidity': '{0:0.1f}'.format(humidity)
            }

        return None

    def celsiusToFahrenheit(self,fahreinheit_temp):
        return fahreinheit_temp * 9/5 + 32
