import adafruit_irremote
from pulseio import PulseOut, PulseIn
from board import IR_TX, D5

class ir_shelfstate():
    def __init__(self):
        self.pulseout = PulseOut(IR_TX, frequency=38000, duty_cycle=2 ** 15)
        self.encoder = adafruit_irremote.GenericTransmit(header=[9000, 4500], one=[560, 1700], zero=[560, 560], trail=0)
        self.ir_receiver = PulseIn(D5, maxlen=120, idle_state=True)
        self.decoder = adafruit_irremote.GenericDecode()


    def transmit(self, shelf_state, phone_state):
        self.encoder.transmit((self.pulseout, [255, 2, shelf_state, phone_state]))

    def receive(self):
        # this method is called in while loop
        pulses = self.decoder.read_pulses(self.ir_receiver)
        try:
            # Attempt to decode the received pulses
            received_code = self.decode_ir_signals(pulses)
            if received_code:
                hex_code = ''.join(["%02X" % x for x in received_code])
            return hex_code
        except adafruit_irremote.IRNECRepeatException:  # Signal was repeated, ignore
            pass
        except adafruit_irremote.IRDecodeException:  # Failed to decode signal
            print("Error decoding")