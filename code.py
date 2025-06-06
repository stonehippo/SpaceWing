import time
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306

# from adafruit_display_text import label
from adafruit_bmp3xx import BMP3XX_I2C as BMP3XX
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from adafruit_gps import GPS

i2c = board.I2C()

displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=32)  # set up the OLED display

bmp = BMP3XX(i2c)  # set up the pressure + temperature sensor

accel_gyro = LSM6DS(i2c)  # set up the accelerometer + gyroscope
mag = LIS3MDL(i2c)  # set up the magnetometer

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

gps = GPS(uart, debug=False)  # set up the GPS with I2C (rather than UART)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")  # set GPS update rate to 1Hz

# main loop
last_print = time.monotonic()

def prep_display():
    display_group = displayio.Group()
    color_bitmap = displayio.Bitmap(128, 32, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    display_group.append(bg_sprite)
    return display_group

def update_display_temp_pressure(temperature, pressure):
    display_group = prep_display()
    temp_text ="Temp: %0.1f F/ %0.1f C" % ((temperature * 1.8 + 32), temperature)
    pressure_text = "Pressure: %0.1f kPa" % pressure

    temp_lbl = label.Label(terminalio.FONT, text = temp_text, color=0xFFFFFF, x=1, y=8)
    pressure_lbl = label.Label(terminalio.FONT, text = pressure_text, color=0xFFFFFF, x=1, y=22)

    display_group.append(temp_lbl)
    display_group.append(pressure_lbl)
    display.root_group = display_group

def update_display_location(longitude, latitude):
    display_group = prep_display()
    longitude_text = "Long: {:.6f}".format(gps.longitude)
    latitude_text = "Lat: {:.6f}".format(latitude)

    longitude_lbl = label.Label(terminalio.FONT, text=longitude_text, color=0xFFFFFF, x=1, y=8)
    latitude_lbl = label.Label(terminalio.FONT, text=latitude_text, color=0xFFFFFF, x=1, y=22)

    display_group.append(longitude_lbl)
    display_group.append(latitude_lbl)
    display.root_group = display_group

def update_no_gps_fix():
    display_group = prep_display()

    lbl = label.Label(terminalio.FONT, text="Waiting for GPS fix...", color=0xFFFFFF, x=1, y=8)

    display_group.append(lbl)
    display.root_group = display_group

# overall time for updating
update_interval = 8.0

# To-do
# - read the state of the buttons
# - set display and update mode based on buttons
# - use GPS RTC to display time
# - animate compass

while True:
    gps.update()

    current = time.monotonic()
    # set the display update to happen once per second or so
    if current - last_print > update_interval:
        acceleration = accel_gyro.acceleration
        gyro = accel_gyro.gyro
        magnetic = mag.magnetic
        last_print = current

        update_display_temp_pressure(bmp.temperature, bmp.pressure)
        time.sleep(update_interval/2.0)
        if gps.has_fix:
            update_display_location(gps.longitude, gps.latitude)
        else:
            update_no_gps_fix()
        # uncomment to print to the console
        #print("Accel: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*acceleration))
        #print("Gyro: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*gyro))
        #print("Mag: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} uT".format(*magnetic))
        #print(" ")