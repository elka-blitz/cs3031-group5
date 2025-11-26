from board import A0
from neopixel import NeoPixel

class led_controller:
    
    def __init__(self):
        self.pixel_amount = 12
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.dormant = (0, 0, 0)
        self.progress = (255, 170, 1)
        self.pixels = NeoPixel(A0,self.pixel_amount,brightness=0.1,auto_write=True)

    def update_lights(self, study_finished):
        if study_finished:
            self.pixels.fill(self.green)
        else:
            self.pixels.fill(self.red)

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
