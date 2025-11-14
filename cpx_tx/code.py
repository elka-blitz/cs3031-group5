import time
import pulseio
from board import IR_TX

from nfc_reader import nfc_reader
from led_controller import sonar

import adafruit_irremote

# Create a 'PulseOut' to send infrared signals on the IR transmitter @ 38KHz
pulseout = pulseio.PulseOut(IR_TX, frequency=38000, duty_cycle=2**15)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1700], zero=[560, 560], trail=560
)

nfc = nfc_reader(None, [], 4) # pass None here instead of '0x80 if wildcard is unknown'
ext_ring_and_prox_sensor = sonar()


while True:

    drawer_closed = ext_ring_and_prox_sensor.is_closed() 
    phone_placed = nfc.getPhoneState()
    signal = [255, 2, phone_placed, drawer_closed] 
    encoder.transmit(pulseout, signal)
    print(signal)
    time.sleep(1)