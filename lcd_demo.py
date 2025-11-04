'''
LCD class demo script

Place code in code.py

Ensure board and busio modules present
'''

from lcd16x2 import LCD_16x2
import time

lcd = LCD_16x2()

while True:
    lcd.display_message('Wassup', line_2='world')
    time.sleep(2)
    lcd.display_message('testing 1, 2, 1, 1', line_2='Bottom text')
    time.sleep(2)
    lcd.clear_lcd()
