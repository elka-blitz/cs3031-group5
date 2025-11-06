import time
import board
import adafruit_hcsr04
import neopixel


class led_controller:
    # replace A? with whatever clips are attached to pins for proximity
    def __init__(self):
        self.pixel_amount = 12
        self.pixels = neopixel.NeoPixel(board.A1,self.pixel_amount,brightness=0.4,auto_write=True)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.dormant = (0, 0, 0)
        self.progress = (255, 170, 1)
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A4, echo_pin=board.A5)


    def update_lights(self, study_finished):
            try:
                distance = self.sonar.distance
                print("Distance", distance, "cm")
                if distance <= 5:
                    # update_progress(call in function_variable) -> don't need the next line if we are showing continous progress
                    self.pixels.fill(self.dormant)
                    print("study in progress")
                else:
                    if study_finished:
                        self.pixels.fill(self.green)
                        print("Study finished")
                    else:
                        self.pixels.fill(self.red)
                        print("Study unfinished")
                time.sleep(2)

            except RuntimeError:
                print("Sensor error = retrying...")
                time.sleep(0.1)

    def update_progress(self, value):
# requires max, global value instead of dividing by 10
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
            time.sleep(2)
        except Exception as e:
            print("Error updating progress:", e)
            time.sleep(0.1)
