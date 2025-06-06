import time
import board

from adafruit_ble import BLERadio

from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as LSM6DS

# set up the accelerometer + gyroscope
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)

# set up the radio hardware
ble = BLERadio()

# By default, your device will have some name like CIRCUITPYxxxx; let's make that more user friendly
ble.name = "MyCPDevice"

# set up the UART service. This virtual serial port lets you send text over BLE.
uart = UARTService()

# set up advertising, so your phone or PC will know that UART service is available on your device
advertisement = ProvideServicesAdvertisement(uart)

while True:
  print("Advertising BLE services")
  # start advertising
  ble.start_advertising(advertisement)
  # keep going until we get a connection
  while not ble.connected:
    pass
    
  # if we got here, we have a connection. Stop advertising!
  ble.stop_advertising()
  print("BLE connected")
  
  # do some work as long as we're connected
  while ble.connected:
    x, y, z = accel_gyro.acceleration
    plot_data = f"{x}, {y}, {z}\n"
    uart.write(plot_data.encode("utf-8"))
    time.sleep(0.025)
  
  # we no longer have a connection, so we'll go back to the top of the loop
  # and start advertising again
  print("BLE disconnected")
