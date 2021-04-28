# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example uses the slide switch to control the little red LED."""
import time
# import neopixel libraries conflicted with the cp library
# import board
# import digitalio
# import busio
from adafruit_circuitplayground import cp

# This code is written to be readable versus being Pylint compliant.
# pylint: disable=simplifiable-if-statement

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
ble = adafruit_ble.BLERadio()
ble.name = "Bluefruit-Volume-Control"
# Using default HID Descriptor.
hid = HIDService()
device_info = DeviceInfoService(
    software_revision=adafruit_ble.__version__, manufacturer="Adafruit Industries"
)
advertisement = ProvideServicesAdvertisement(hid)
cc = ConsumerControl(hid.devices)

# Intialize different color specifications
# for the neopixels depending on the status of the device
FILL_COLOR = (0, 32, 32)
UNMUTED_COLOR = (0, 128, 128)
MUTED_COLOR = (128, 0, 0)
DISCONNECTED_COLOR = (40, 40, 0)
ALARM_COLOR = (128, 0, 0)
MOVE_THRESHOLD = 50

# set neopixels to state before bluetooth is connected
# ring = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.05, auto_write=False)
# ring.fill(DISCONNECTED_COLOR)
# ring.show()
cp.pixels.brightness = 0.05
cp.pixels.fill(DISCONNECTED_COLOR)

muted = False
command = None
# Disconnect if already connected, so that we pair properly.
if ble.connected:
    for connection in ble.connections:
        connection.disconnect()


def draw():
    if not muted:
        # ring.fill(FILL_COLOR)
        cp.pixels.fill(FILL_COLOR)
        # ring[dot_location] = UNMUTED_COLOR
    else:
        cp.pixels.fill(MUTED_COLOR)
    # ring.show()


advertising = False
connection_made = False
print("let's go!")

while True:
    ON = cp.switch
    if cp.button_a:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
    if ON:
        cp.red_led = True
        if not ble.connected:
            cp.pixels.fill(DISCONNECTED_COLOR)
            # ring.show()
            connection_made = False
            if not advertising:
                ble.start_advertising(advertisement)
                advertising = True
            continue
        else:
            if connection_made:
                pass
            else:
                cp.pixels.fill(FILL_COLOR)
                # ring.show()
                connection_made = True
        advertising = False
        x, y, z = cp.acceleration
        print((x, y, z))
        L_stored = ((x**2)+(y**2)+(z**2))**0.5
        print("Stored Magnitude")
        print((L_stored))
        time.sleep(0.3)
        x_new, y_new, z_new = cp.acceleration
        print((x_new, y_new, z_new))
        L_new = ((x_new**2)+(y_new**2)+(z_new**2))**0.5
        print("New Magnitude")
        print((L_new))
        if abs(10*L_new - 10*L_stored) > MOVE_THRESHOLD:
            cp.pixels.fill(ALARM_COLOR)
            # ring.show()
            cc.send(ConsumerControlCode.PLAY_PAUSE)
            for i in range(1,16):
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            time.sleep(0.5)
            ON = False
    else:
        cp.red_led = False
        cp.pixels.fill((0, 0, 0))
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
