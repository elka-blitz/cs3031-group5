import adafruit_irremote
import pulseio
import board

# # Create a 'pulseio' output, to send infrared signals on the IR transmitter @ 38KHz
# pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
# # Create an encoder that will take numbers and turn them into NEC IR pulses
# encoder = adafruit_irremote.GenericTransmit(header=[9000, 4500],
#                                             one=[560, 1700],
#                                             zero=[560, 560],
#                                             trail=0)

# while True:
#     if cpx.button_a:
#         print("Button A pressed! \n")
#         cpx.red_led = True
#         encoder.transmit(pulseout, [255, 2, 255, 0])
#         cpx.red_led = False
#         # wait so the receiver can get the full message
#         time.sleep(0.2)
#     if cpx.button_b:
#         print("Button B pressed! \n")
#         cpx.red_led = True
#         encoder.transmit(pulseout, [255, 2, 191, 64])
#         cpx.red_led = False
#         time.sleep(0.2)

class ir_shelfstate():
    def __init__(self):
        self.pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
        self.encoder = adafruit_irremote.GenericTransmit(header=[9000, 4500], one=[560, 1700], zero=[560, 560], trail=0)
        self.ir_receiver = pulseio.PulseIn(board.D5, maxlen=120, idle_state=True)
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
            print(f"Received: {hex_code}")
        except adafruit_irremote.IRNECRepeatException:  # Signal was repeated, ignore
            pass
        except adafruit_irremote.IRDecodeException:  # Failed to decode signal
            print("Error decoding")