from time import sleep
from board import A3, A4, A5
from adafruit_hcsr04 import HCSR04
from neopixel import NeoPixel


class led_controller:
    
    def __init__(self):
        self.pixel_amount = 12
        self.pixels = NeoPixel(A3,self.pixel_amount,brightness=0.4,auto_write=True)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.dormant = (0, 0, 0)
        self.progress = (255, 170, 1)
        self.sonar = HCSR04(trigger_pin=A4, echo_pin=A5)

    def is_closed(self):
        if self.sonar.distance >= 5:
            return False
        else:
            return True

    def update_lights(self, study_finished):
            try:
                distance = self.sonar.distance
                print("Distance", distance, "cm")
                if distance <= 5:
                    
                    self.pixels.fill(self.dormant)
                    print("study in progress")
                else:
                    if study_finished:
                        self.pixels.fill(self.green)
                        print("Study finished")
                    else:
                        self.pixels.fill(self.red)
                        print("Study unfinished")
                sleep(2)

            except RuntimeError:
                print("Sensor error = retrying...")
                sleep(0.1)

    def update_progress(self, value):

        try:
            percentage = (value/10) * 100
            rounded_percentage = round(percentage / 10) * 10
            pixels_lit = int((rounded_percentage / 100) * self.pixel_amount)
            for i in range(self.pixel_amount):
                if i < pixels_lit:
                    self.pixels[i] = self.progress
                else:
                    self.pixels[i] = self.dormant
            print(f"Value: {value} -> ({rounded_percentage} % -> {pixels_lit} pixels lit")
            sleep(2)
        except Exception as e:
            print("Error updating progress:", e)
            sleep(0.1)
