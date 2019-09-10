import math
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


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
font = ImageFont.truetype('FreeMono.ttf', 18)

# Create drawing object.
draw = ImageDraw.Draw(image)
char_width, char_height = draw.textsize('A', font=font)

# Define text and get total width.
text = 'HAROLD LOVES SHANNON'
maxwidth, unused = draw.textsize(text, font=font)

# Set animation and sine wave parameters.
amplitude = height/4
offset = height/2 - 4
velocity = -16
startpos = width

# Animate text moving in sine wave.
print('Press Ctrl-C to quit.')
pos = startpos

# Clear image buffer by drawing a black filled box.
draw.rectangle((0,0,width,height), outline=0, fill=0)

while True:
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(image)
    disp.display()
    time.sleep(0.5)

    draw.text((5, 0), 'HAROLD', font=font, fill=255)
    disp.image(image)
    disp.display()

    time.sleep(0.5)

    draw.text((5, char_height * 1), 'LOVES', font=font, fill=255)
    disp.image(image)
    disp.display()

    time.sleep(0.5)

    draw.text((5, char_height * 2), 'SHANNON', font=font, fill=255)
    disp.image(image)
    disp.display()

    time.sleep(0.5)

while False:
    # Enumerate characters and draw them offset vertically based on a sine wave.
    x = pos
    for i, c in enumerate(text):
        # Stop drawing if off the right side of screen.
        if x > width:
            break
        # Calculate width but skip drawing if off the left side of screen.
        if x < -10:
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
            continue
        # Calculate offset from sine wave.
        #y = offset+math.floor(amplitude*math.sin(x/float(width)*2.0*math.pi))
        # Draw text.
        draw.text((x, height//2), c, font=font, fill=255)
        # Increment x position based on chacacter width.
        char_width, char_height = draw.textsize(c, font=font)
        x += char_width
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    # Move position for next frame.
    pos += velocity
    # Start over if text has scrolled completely off left side of screen.
    if pos < -maxwidth:
        pos = startpos
    # Pause briefly before drawing next frame.
    time.sleep(0.1)
