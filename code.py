from lcd16x2 import LCD_16x2
import time
from adafruit_circuitplayground.express import cpx
from navbuttons import group5StudyAssistantNavigation

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
START_TIME = 0
TIME_SESSION_COMPLETE = False

lcd = LCD_16x2()
nav = group5StudyAssistantNavigation()

# --------- Main Loop ---------------- #
while True:
    time.sleep(0.5)

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

    if drawer_closed and phone_placed and not TIME_SESSION_COMPLETE:
        # Display countdown 3
        # It's showtime

        if TIME_SET != True: # This should only be done once per shelf close
            TIME_AMOUNT_SET = TIME_NAV # In seconds for testing, multiply by 60 when testing complete
            TIME_SET = True
            START_TIME = time.time()

        elapsed_time = time.time() - START_TIME
        remaining_time = round(((TIME_AMOUNT_SET - elapsed_time) / 60) * 100)
        remaining_time_percentage = round(remaining_time / TIME_AMOUNT_SET) # Pass this to external neopixel ring class
        if remaining_time < 0:
            TIME_SESSION_COMPLETE = True

        DO_ANIMATION = False # No need for cycle, frame will update with time every second

        lcd.display_message('Studying...', line_2=str(remaining_time))

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

        if TIME_SESSION_COMPLETE:
            DO_ANIMATION = True
            if ANIMATION_CYCLE != ANIMATION_UPDATE:
                ANIMATION_UPDATE = ANIMATION_CYCLE

                if ANIMATION_CYCLE:
                    lcd.display_message('Session complete')
                else:
                    lcd.display_message('Open shelf', line_2='to restart')
                break

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
            # Hey, would be cool to show touch feedback on external neopixel ring for the two touch pins?
            # If they could display faster than the refresh rate for more immediate feedback
            TIME_NAV += 5
            lcd.display_message('Set time:', line_2=str(TIME_NAV))

        if nav.touch_a2():
            if TIME_NAV - 5 > 1: # Prevent negative numbers
                TIME_NAV = TIME_NAV - 5
            lcd.display_message('Set time:', line_2=str(TIME_NAV))

        if ANIMATION_CYCLE != ANIMATION_UPDATE:
            ANIMATION_UPDATE = ANIMATION_CYCLE
            lcd.display_message('Set time:', line_2=str(TIME_NAV))

        
# Match timer set?