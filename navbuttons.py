'''
Buttons are boring
All my homies hate buttons

Using metal objects instead of dedicated button technology?
Now that's ubicomp!
Now we're thinking with portals
'''
from adafruit_circuitplayground.express import cpx
import time
import touchio
import board

class group5StudyAssistantNavigation():
    def __init__(self):
        self.var1 = 0 # Super descriptive variable
        cpx.pixels.brightness = 0.1
        self.touch_A1 = touchio.TouchIn(board.A1)


    def touch(self):
        if self.touch_A1.raw_value > 3000:
            return True
        else:
            return False
    
