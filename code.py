from lcd16x2 import LCD_16x2
from time import sleep, time
from adafruit_circuitplayground.express import cpx
from navbuttons import group5StudyAssistantNavigation
from led_controller import led_controller
from nfc_reader import nfc_reader

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

while True:
    sleep(0.5)
    if DO_ANIMATION: 
        ANIMATION_FRAME_TICK += 1
    if ANIMATION_FRAME_TICK > FRAME_LENGTH:
        ANIMATION_CYCLE = not ANIMATION_CYCLE 
        ANIMATION_FRAME_TICK = 0
    drawer_closed = False 
    phone_placed = True 

    if drawer_closed and phone_placed and not TIME_SESSION_COMPLETE:
        if TIME_SET != True: 
            TIME_AMOUNT_SET = TIME_NAV 
            TIME_SET = True
            START_TIME = time()
        elapsed_time = time() - START_TIME
        remaining_time = round(((TIME_AMOUNT_SET - elapsed_time) / 60) * 100)
        remaining_time_percentage = round(remaining_time / TIME_AMOUNT_SET) 
        if remaining_time < 0:
            TIME_SESSION_COMPLETE = True
        DO_ANIMATION = False 
        lcd.display_message('Studying...', line_2=str(remaining_time))

    elif not drawer_closed and not phone_placed:     
        DO_ANIMATION = True
        if ANIMATION_CYCLE != ANIMATION_UPDATE:
            ANIMATION_UPDATE = ANIMATION_CYCLE
            if ANIMATION_CYCLE:
                lcd.display_message('Place phone', line_2='in shelf')
            else:
                lcd.display_message('To start', line_2='study session')

    elif drawer_closed:      
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
        DO_ANIMATION = False
        if nav.touch_a1():    
            TIME_NAV += 5
            lcd.display_message('Set time:', line_2=str(TIME_NAV))
        if nav.touch_a2():
            if TIME_NAV - 5 > 1: 
                TIME_NAV = TIME_NAV - 5
            lcd.display_message('Set time:', line_2=str(TIME_NAV))
        if ANIMATION_CYCLE != ANIMATION_UPDATE:
            ANIMATION_UPDATE = ANIMATION_CYCLE
            lcd.display_message('Set time:', line_2=str(TIME_NAV))