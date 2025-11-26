from board import REMOTEIN
from pulseio import PulseIn
from adafruit_irremote import GenericDecode, IRDecodeException, IRNECRepeatException
from gc import collect


class ir_shelfstate():
    def __init__(self):
        print('ir init')
        self.pulsein = PulseIn(REMOTEIN, maxlen=40)
        self.decoder = GenericDecode()
        self.tx_map = {'(224, 32, 1)':[True, True], '(224, 32, 0)':[True, False], '(224, 0, 0)':[False, False], '(224, 0, 1)':[False, True]}
        

    def receive(self):
        # pulses.clear()
        self.pulsein.pause()
        print(len(self.pulsein))
        if len(self.pulsein) > 0:
            try:
                print('trying pulse')
                pulse = self.decoder.read_pulses(self.pulsein)
                print('\033[92mPulse read success\033[0m')
                try:

                    code = self.decoder.decode_bits(pulse)
                    print('\033[1m\033[92mDecode success\033[0m', code)

                    translation = self.tx_map[str(code)]
                    self.pulsein.clear()
                    return translation
                except IRDecodeException:
                    print('\033[93mEncode Decode fail\033[0m')
                except KeyError:
                    print('\033[93mTranslation failed\033[0m')
                except MemoryError:
                    collect()
                    print('\033[4m\033[1m\033[91mMemory Error\033[0m')
                    self.pulsein.clear()

                return pulse
            except RuntimeError:
                print('\033[93mRuntimeError\033[0m')
                self.pulsein.clear()
                raise RuntimeError
            except IRNECRepeatException:  # unusual short code!
                print('\033[93mShort code\033[0m')
                raise IRNECRepeatException
            except IRDecodeException:  # Failed to decode signal
                print('\033[93mDecode fail\033[0m')
                raise IRDecodeException

            print(pulse)
        self.pulsein.clear
        self.pulsein.resume()