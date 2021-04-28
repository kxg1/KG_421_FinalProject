# Keeler Gonzales, Rice University, Department of Bioengineering
# BIOE 421 Microcontroller Applications
# Bluetooth-car alarm device

# import necessary libraries for time delays and circuit playground functions
import time
from adafruit_circuitplayground import cp

# Import libraries necessary for control of iPhone
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
# Import libraries for bluetooth connection
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
ble = adafruit_ble.BLERadio()
ble.name = "Bluefruit-Car-Alarm"
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
cp.pixels.brightness = 0.05
cp.pixels.fill(DISCONNECTED_COLOR)

# Disconnect if already connected, so that we pair properly.
if ble.connected:
    for connection in ble.connections:
        connection.disconnect()
advertising = False
connection_made = False
# loop to run continuously
while True:
    MOVE_THRESHOLD = 50
    delay_time = 10
    while True:
        ON = cp.switch
        # the slide switch operates the device on/off
        if ON:
            print("Armed and Ready")
            cp.red_led = True
            # when turned on, the device initially
            # detects whether bluetooth is connected
            if not ble.connected:
                cp.pixels.fill(DISCONNECTED_COLOR)
                # A specific ring color is shown when device is disconnected
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
                    connection_made = True
                    # when a connection
                    # is made, device lights up blue and advertising halts
            advertising = False
            if not advertising:
                cp.pixels.fill(FILL_COLOR)
            # This section takes in the boards acceleration data, and calculates
            # the magnitude of 2 vectors .3 seconds apart from each other
            # If the difference between these two vectors is greater than a
            # specified move threshold, then the alarm is triggered
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
            # The alarm works by playing a set alarm on the connected burner phone,
            # and turning the volume all the way up
            if abs(10*L_new - 10*L_stored) > MOVE_THRESHOLD:
                cp.pixels.fill(ALARM_COLOR)
                cc.send(ConsumerControlCode.PLAY_PAUSE)
                for i in range(1, 20):
                    cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                MOVE_THRESHOLD += 500
                time.sleep(delay_time)
                break
                # after an alarm goes off, the threshold increases
                # by a lot so it isnt triggered again and
                # accidentally pauses the alarm
                # the delay can be adjusted based on
                # how far away someone is from their car

        else:
            cp.red_led = False
            cp.pixels.fill((0, 0, 0))
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            Calibrate = cp.button_a
            time.sleep(0.3)
            # volume is continuously decreased when not armed
            print(Calibrate)
            # status of alarm can be manually turned on and off,
            # because it might end up in the wrong state after a trigger
            if Calibrate:
                cc.send(ConsumerControlCode.PLAY_PAUSE)
                time.sleep(0.1)
                Calibrate = False
            time.sleep(0.3)
            # buttons used to toggle sensitivty and delay of alarm
            if cp.button_b:
                MOVE_THRESHOLD += 1
            if cp.touch_A1:
                MOVE_THRESHOLD -= 1
            print("movement threshold", MOVE_THRESHOLD)
            if cp.touch_A2:
                delay_time += 1
            if cp.touch_A3:
                delay_time -= 1
            print("delay time for alarm", delay_time)
            time.sleep(0.3)




