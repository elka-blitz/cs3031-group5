from board import A6, A7
from adafruit_hcsr04 import HCSR04
from neopixel import NeoPixel


class led_controller:
    
    def __init__(self):
        self.sonar = HCSR04(trigger_pin=A6, echo_pin=A7)

    def is_closed(self):
        if self.sonar.distance >= 5:
            return False
        else:
            return True