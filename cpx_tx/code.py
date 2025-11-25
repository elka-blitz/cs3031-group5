import time
import pulseio
from board import IR_TX

from nfc_reader import nfc_reader
from led_controller import led_controller

import adafruit_irremote

# Create a 'PulseOut' to send infrared signals on the IR transmitter @ 38KHz
pulseout = pulseio.PulseOut(IR_TX, frequency=38000, duty_cycle=2**15)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1700], zero=[560, 560], trail=560
)

transmit_sensors = True
nfc_found = True

try:
    nfc = nfc_reader(None, [], 4) # pass None here instead of '0x80 if wildcard is unknown'
except:
    nfc_found = False
    phone_placed = True
    print("No NFC reader detected. Switching to proximity only.")

try:
    prox_sensor = led_controller()
except:
    transmit_sensors = False
    print("No proximity sensor detected. Exiting")

while transmit_sensors:

    drawer_closed = prox_sensor.is_closed() 
    if nfc_found:
        phone_placed = nfc.getPhoneState()

    encoder.transmit(pulseout, [phone_placed, drawer_closed])
    print("Transmitting:",str(phone_placed, drawer_closed))
    time.sleep(1)