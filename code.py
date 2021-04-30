import time
import board
import busio
import adafruit_bus_device
import displayio
from adafruit_displayio_ssd1306 import SSD1306
from adafruit_display_text import label
from adafruit_bmp3xx import BMP3XX_I2C as BMP3XX
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from adafruit_gps import GPS

i2c = board.I2C()

displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = SSD1306(display_bus, width=128, height=32) 				# set up the OLED display

bmp = BMP3XX(i2c)					# set up the pressure + temperature sensor

accel_gyro = LSM6DS(i2c)			# set up the accelerometer + gyroscope
mag = LIS3MDL(i2c)					# set up the magnetometer

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

gps = GPS(uart, debug=False)		# set up the GPS with I2C (rather than UART)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")	#configure basic GGA and RMC info
gps.send_command(b"PMTK220,1000")	# set GPS update rate to 1Hz

# main loop
last_print = time.monotonic()
while True:
	gps.update()
	
	current = time.monotonic()
	if current - last_print > 1.0:	# set the display update to happen once per second or so
		acceleration = accel_gyro.acceleration
		gyro =accel_gyro.gyro
		magnetic = mag.magnetic

# uncomment to print to the console		
# 		if not gps.has_fix:
# 			print("Waiting for GPS fix...")
# 			continue
# 		print("Lat: {:.6f} Long: {:.6f} Qual: {:d}".format(gps.latitude, gps.longitude, gps.fix_quality))
# 		print("Accel: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*acceleration))
# 		print("Gyro: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*gyro))
# 		print("Mag: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} uT".format(*magnetic))
# 		print("Pressure: {:6.4f} Temp: {:5.2f}".format(bmp.pressure, bmp.temperature))
# 		print(" ")
