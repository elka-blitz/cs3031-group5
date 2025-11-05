'''
Proposed main process to integrate all sensors and actuators
'''
from lcd16x2 import LCD_16x2
import time
from adafruit_circuitplayground.express import cpx
from navbuttons import group5StudyAssistantNavigation
import board

import adafruit_hcsr04

cpx.pixels.brightness = 0.1

STUDY_ASSISTANT_STATE = 0

DO_ANIMATION = True
ANIMATION_CYCLE = False
ANIMATION_FRAME_TICK = 0
ANIMATION_UPDATE = True
FRAME_LENGTH = 1

TIME_SET = False
TIME_NAV = 20
TIME_AMOUNT_SET = 0


lcd = LCD_16x2()
nav = group5StudyAssistantNavigation()

# --------- Main Loop ---------------- #
while True:
    time.sleep(1)

    if DO_ANIMATION: # Prevent unneccesary screen refresh where animation tick drive not needed
        ANIMATION_FRAME_TICK += 1

    if ANIMATION_FRAME_TICK > FRAME_LENGTH:
        ANIMATION_CYCLE = not ANIMATION_CYCLE # Do a flip
        ANIMATION_FRAME_TICK = 0

    # Check sensor states
    drawer_closed = False # Replace with sensor method
    phone_placed = True # Replace with sensor method

    # Determine system state
    # This could be optimised somehow, see duplicated code
    # Either: Idle, Phone not Detected, Phone Detected, Countdown
    # 0, 1, 2, 3

    if drawer_closed and phone_placed:
        # Display countdown 3
        pass

    elif not drawer_closed and not phone_placed:
        # Idle state 0

        DO_ANIMATION = True
        if ANIMATION_CYCLE != ANIMATION_UPDATE:
            ANIMATION_UPDATE = ANIMATION_CYCLE

            if ANIMATION_CYCLE:
                lcd.display_message('Place phone', line_2='in shelf')
            else:
                lcd.display_message('To start', line_2='study session')

    elif drawer_closed:
        # Phone not detected 1
        DO_ANIMATION = True
        if ANIMATION_CYCLE != ANIMATION_UPDATE:
            ANIMATION_UPDATE = ANIMATION_CYCLE

            if ANIMATION_CYCLE:
                lcd.display_message('Phone not', line_2='in shelf')
            else:
                lcd.display_message('Place phone in', line_2='shelf to start')

    else:
        # Shelf not closed 0
        # Timer set state
        DO_ANIMATION = False
        # Update if change in TIME_NAV detected
        if nav.touch_a1():
            TIME_NAV += 5
            lcd.display_message('Set time:', line_2=str(TIME_NAV))

        if nav.touch_a2():
            if TIME_NAV - 5 > 5: # Prevent negative numbers
                TIME_NAV = TIME_NAV - 5
            lcd.display_message('Set time:', line_2=str(TIME_NAV))

        if ANIMATION_CYCLE != ANIMATION_UPDATE:
            ANIMATION_UPDATE = ANIMATION_CYCLE
            lcd.display_message('Set time:', line_2=str(TIME_NAV))

        pass

        
# Match timer set?
