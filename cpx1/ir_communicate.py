import adafruit_irremote
import pulseio
import board

class infrared_i2c():
    def __init__(self):
        # Create a 'pulseio' output, to send infrared signals on the IR transmitter @ 38KHz
        self.pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
        # Create an encoder that will take numbers and turn them into NEC IR pulses
        self.encoder = adafruit_irremote.GenericTransmit(header=[9000, 4500],
                                                    one=[560, 1700],
                                                    zero=[560, 560],
                                                    trail=0)
        self.pulses = decoder.read_pulses(pulsein)

        def transmit_state(self, state):
            self.encoder.transmit(pulseout, [255, 2, state1, state2])
            
        def receive_state(self):
            try:
                # Attempt to convert received pulses into numbers
                received_code = decoder.decode_bits(pulses)
            # We got an unusual short code, probably a 'repeat' signal
            # print("NEC repeat!")
            continue

            except adafruit_irremote.IRDecodeException as e:
                # Something got distorted or maybe its not an NEC-type remote?
                # print("Failed to decode: ", e.args)
                continue

                if received_code == [255, 2, 255, 0]:
        print("Received NEC Vol-")
    if received_code == [255, 2, 127, 128]:
        print("Received NEC Play/Pause")
    if received_code == [255, 2, 191, 64]:
        print("Received NEC Vol+")

