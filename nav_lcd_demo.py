from lcd16x2 import LCD_16x2
import time
from adafruit_circuitplayground.express import cpx
from navbuttons import group5StudyAssistantNavigation

cpx.pixels.brightness = 0.1

lcd = LCD_16x2()
nav = group5StudyAssistantNavigation()
touch = False

while True:
    touch_check = nav.touch()

    # Hanoi check if change 
    if touch_check != touch:
        touch = touch_check
        # Update screen
        lcd.clear_lcd()
        lcd.display_message(str(touch))

    time.sleep(0.2)
