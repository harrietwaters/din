from RPi import GPIO
import time

GPIO.setup

GPIO.setmode(GPIO.BCM)

relay_pins = {17, 27, 22, 10}

for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)

while True:
    for pin in relay_pins:
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
    for pin in relay_pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)