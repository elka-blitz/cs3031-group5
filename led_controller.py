from board import A0, A6, A7
from adafruit_hcsr04 import HCSR04
from neopixel import NeoPixel


class led_controller:
    
    def __init__(self):
        self.pixel_amount = 12
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.dormant = (0, 0, 0)
        self.progress = (255, 170, 1)
        self.pixels = NeoPixel(A0,self.pixel_amount,brightness=0.1,auto_write=True)
        self.sonar = HCSR04(trigger_pin=A6, echo_pin=A7)

    def is_closed(self):
        if self.sonar.distance >= 5:
            return False
        else:
            return True

    def update_lights(self, study_finished):
            try:
                distance = self.sonar.distance
                if distance <= 5:
                    
                    self.pixels.fill(self.dormant)
                else:
                    if study_finished:
                        self.pixels.fill(self.green)
                    else:
                        self.pixels.fill(self.red)

            except RuntimeError:
                print("Sensor error = retrying...")

    def update_progress(self, value):

        try:
            percentage = value * 100
            rounded_percentage = round(percentage / 10) * 10
            pixels_lit = int((rounded_percentage / 100) * self.pixel_amount)
            for i in range(self.pixel_amount):
                if i < pixels_lit:
                    self.pixels[i] = self.progress
                else:
                    self.pixels[i] = self.dormant
            print(f"Value: {value} -> ({rounded_percentage} % -> {pixels_lit} pixels lit")
        except Exception as e:
            print("Error updating progress:", e)
