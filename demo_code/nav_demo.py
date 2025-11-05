import touchio
import board
import time
from adafruit_circuitplayground.express import cpx
from navbuttons import group5StudyAssistantNavigation


cpx.pixels.brightness = 0.1

'''
Buttons but cool
Check for the pin raw values
3000 seems to signify human touch
Check raw value every main process cycle and act from there
Example commented below
'''
nav = group5StudyAssistantNavigation()

while True:
    print(nav.touch())
    time.sleep(1)
