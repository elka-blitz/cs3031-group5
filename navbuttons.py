from adafruit_circuitplayground.express import cpx
import time
import touchio
import board

class group5StudyAssistantNavigation():
    def __init__(self):
        self.var1 = 0
        cpx.pixels.brightness = 0.1
        self.touch_A1 = touchio.TouchIn(board.A1)
        self.touch_A2 = touchio.TouchIn(board.A2)


    def touch_a1(self):
        if self.touch_A1.raw_value > 3000:
            return True
        else:
            return False
        
    def touch_a2(self):
        if self.touch_A2.raw_value > 3000:
            return True
        else:
            return False