import json
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

pin = 4

def read_climate:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        tempObj = {}

        if humidity is not None and temperature is not None:
            temperature = temperature * 9/5 + 32
            tempObj = {
                    'temp': '{0:0.1f}'.format(temperature, humidity),
                    'humidity': '{1:0.1f}'.format(temperature, humidity)
            }

            print(json.dumps(tempObj))
            with open('climate.json', 'w') as fp:
                json.dump(tempObj, fp)

        time.sleep(2)

read_climate()
