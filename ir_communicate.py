import adafruit_irremote
from pulseio import PulseIn
from board import REMOTEIN

class ir_shelfstate():
    def __init__(self):
        print('ir init')
        self.pulsein = PulseIn(REMOTEIN, maxlen=40, idle_state=True)
        self.decoder = adafruit_irremote.GenericDecode()

    def receive(self):
        print('receiving')
        # this method is called in while loop
        pulses = self.decoder.read_pulses(self.pulsein)
        print("Heard", len(pulses), "Pulses:", pulses)
        try:
            code = self.decoder.decode_bits(pulses)
            print("Decoded:", code)
        except adafruit_irremote.IRNECRepeatException:  # unusual short code!
            print("NEC repeat!")
        except adafruit_irremote.IRDecodeException:  # Failed to decode signal
            print("Error decoding")
            return None
        except (
            adafruit_irremote.IRDecodeException,
            adafruit_irremote.FailedToDecode,
        ) as e:  # failed to decode
            print("Failed to decode: ", e.args)

        print("----------------------------")