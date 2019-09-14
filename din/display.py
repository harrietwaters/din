import json
import time
import sys

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Raspberry Pi pin configuration:
RST = 24

class Display():
    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

        self.disp.begin()
        self.clear_screen()

        # Load default font.
        self.info_font = ImageFont.truetype('FreeMono.ttf', 12)
        self.curr_temp_font = ImageFont.truetype('FreeMono.ttf', 32)
        self.target_temp_font = ImageFont.truetype('FreeMono.ttf', 16)

        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new('1', (self.disp.width, self.disp.height))

        # Create drawing object.
        self.draw = ImageDraw.Draw(self.image)

        self._curr_temp = '0'
        self._target_temp = '0'
        self._thermostat_mode = 'off'
        self._fan_mode = 'auto'

        self.display_image()

    @property
    def curr_temp(self):
        return self._curr_temp

    @curr_temp.setter
    def curr_temp(self, value):
        #If curr temp is the same, don't bother redrawing
        if self._curr_temp == value:
            return self._curr_temp, True

        self._curr_temp = value
        self.display_image()

        return self._curr_temp, True

    @property
    def target_temp(self):
        return self._target_temp

    @target_temp.setter
    def target_temp(self, value):
        #If target temp is the same, don't bother redrawing
        if self._target_temp == value:
            return self._target_temp

        self._target_temp = value

        self.display_image()

        return self._target_temp, True

    @property
    def thermostat_mode(self):
        return self._thermostat_mode

    @thermostat_mode.setter
    def thermostat_mode(self, value):
        if self._thermostat_mode == value:
            return

        self._thermostat_mode = value

        self.display_image()

        return self._thermostat_mode, True

    @property
    def fan_mode(self):
        return self._fan_mode

    @fan_mode.setter
    def fan_mode(self, value):
        if self._fan_mode == value:
            return
        
        self._fan_mode = value

        self.display_image()

        return self._fan_mode, True

    def display_image(self):
        self.clear_image()

        curr_temp_info_text = 'Current:'
        curr_temp_text = self._curr_temp + '°'

        target_temp_info_text = 'Set to:'
        target_temp_text = self._target_temp.zfill(2) + '°'

        # Current temp
        self.draw.text((0, 0), curr_temp_info_text, font=self.info_font, fill=255)
        self.draw.text((0, 12), curr_temp_text, font=self.curr_temp_font, fill=255)

        # Target temp
        self.draw.text((0, 40), target_temp_info_text, font=self.info_font, fill=255)
        self.draw.text((16, 50), target_temp_text, font=self.target_temp_font, fill=255)

        # Thermostat Mode
        modes = {
            'COOL': 'COOL',
            'HEAT': 'HEAT',
            'OFF':  'OFF '
        }

        modes[self._thermostat_mode.upper()] = modes[self._thermostat_mode.upper()] + '*'

        self.draw.text((90, 0), modes['COOL'], font=self.info_font, fill=255)
        self.draw.text((90, 12), modes['HEAT'], font=self.info_font, fill=255)
        self.draw.text((90, 24), modes['OFF'], font=self.info_font, fill=255)

        # Fan Mode
        fan_modes = {
            'ON': '  ON',
            'AUTO': 'AUTO'
        }

        self.draw.text((70, 40), 'Fan:', font=self.info_font, fill=255)
        self.draw.text((90, 52), fan_modes[self._fan_mode.upper()], font=self.info_font, fill=255)

        self.disp.image(self.image)
        self.disp.display()


    def clear_image(self):
        self.draw.rectangle((0,0,self.disp.width,self.disp.height), outline=0, fill=0)
        self.disp.image(self.image)

    def clear_screen(self):
        self.disp.clear()
        self.disp.display()

    def __del__(self):
        self.clear_screen()