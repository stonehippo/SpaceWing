# SpaceWing

A portable device for location and inertial information, built from Adafruit FeatherWings (plus some other stuff).

## What is SpaceWing?

We are working on a project the involves using GPS for anchoring an augmented reality experience. As part of this development,
I wanted a device that I could use to hack on for various things, including most of the positional sensors available in
smartphones. To get what I wanted, I need GPS, a 9 DoF (accelerometer, gyroscope, and magnetometer), and pressure/altitude.
I also wanted the device to have its own display, plus Bluetooth connectivity so I could offload the sensors readings to
an app on a phone, tablet, or computer.


## Construction

The SpaceWing is built around a Bluetooth enabled Feather nRF52840 Express, with most of the components on
FeatherWings. The Feather and the three component FeatherWings are connected together via a FeatherWing Quad
adapter, while the BMP390 is connected via the STEMMA QT (I2C) port on the 9 DoF IMU FeatherWing.

The LiPoly battery is attached to the back of the quad adapter with some nice Velcro.

## Component Interconnections

Most of the components in the SpaceWing communicate via I2C. The exception is the GPS, which
the nRF52840 talks to over a UART.

## BOM

- [Adafruot Feather nRF52840 Express](https://www.adafruit.com/product/4062)
- [Adafruit Ultimate GPS FeatherWing](https://www.adafruit.com/product/3133)
- [Adafruit FeatherWing OLED - 128x32](https://www.adafruit.com/product/4091)
- [Adafruit ISM330DHCX + LIS3MDL FeatherWing](https://www.adafruit.com/product/4569)
- [Adafruit BMP390L - Precision Barometric Pressure and Altimeter](https://www.adafruit.com/product/4816)
- [Adafruit Quad Side-By-Side FeatherWing Kit with Headers](https://www.adafruit.com/product/4254)
- [STEMMA QT / Qwiic JST SH 4-Pin Cable - 50mm Long](https://www.adafruit.com/product/4399)
- [Lithium Ion Polymer Battery - 3.7v 2500mAh](https://www.adafruit.com/product/328)

## Firmware

I wrote all of the SpaceWing firmware using CircuitPython. See `code.py`.

## Component Guides

The various guides for the components are available below

- [Adafruit Feather nRF52840 Express](https://learn.adafruit.com/introducing-the-adafruit-nrf52840-feather)
- [OLED FeatherWing](https://learn.adafruit.com/adafruit-oled-featherwing)
- [GPS FeatherWing](https://learn.adafruit.com/adafruit-ultimate-gps-featherwing)
- [ISM330DHCX + LIS3MDL FeatherWing](https://learn.adafruit.com/st-9-dof-combo)
- [BMP390 Breakout](https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx)
