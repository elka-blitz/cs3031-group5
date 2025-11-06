from adafruit_circuitplayground.express import cpx
from touchio import TouchIn
from board import A1

class group5StudyAssistantNavigation():
    def __init__(self):
        self.var1 = 0
        cpx.pixels.brightness = 0.1
        self.touch_A1 = TouchIn(A1)


    def touch(self):
        if self.touch_A1.raw_value > 3000:
            return True
        else:
            return False
    
