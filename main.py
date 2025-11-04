import touchio
import board
import time
from adafruit_circuitplayground.express import cpx


touch_A1 = touchio.TouchIn(board.A1)
cpx.pixels.brightness = 0.1

'''
Buttons but cool
Check for the pin raw values
3000 seems to signify human touch
Check raw value every main process cycle and act from there
Example commented below
'''
# while True:
#     raw_value = touch_A1.raw_value
#     if raw_value > 3000:
#         print('touch detected ' + str(raw_value))
#         cpx.pixels.fill([255, 255, 255])
#     else:
#         cpx.pixels.fill([0,0,0])
#     time.sleep(0.1)
