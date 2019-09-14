import json
import time
import sys

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Raspberry Pi pin configuration:
RST = 24

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
#font = ImageFont.load_default()
tempFont = ImageFont.truetype('FreeMono.ttf', 12)
humFont = ImageFont.truetype('FreeMono.ttf', 12)

# Create drawing object.
draw = ImageDraw.Draw(image)
char_width, char_height = draw.textsize('A', font=tempFont)

climate = {}

def main(): 
    while True:
        with open('climate.json', 'r') as fp:
            climate = json.load(fp)
            humidity = climate['humidity']
            temperature = climate['temp']

        if humidity is not None and temperature is not None:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            disp.image(image)

            tempText = 'Temp: {0}*C'.format(temperature)
            humText = 'Humidity: {0}%'.format(humidity)

            draw.text((0, 0), tempText, font=tempFont, fill=255)
            draw.text((0, char_height), humText, font=humFont, fill=255)
            disp.image(image)
            disp.display()

        time.sleep(2)

main()
