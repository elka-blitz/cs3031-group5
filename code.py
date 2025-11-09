from lcd16x2 import LCD_16x2
from led_controller import led_controller
from navbuttons import group5StudyAssistantNavigation
from time import sleep, time

prox = led_controller()
nav = group5StudyAssistantNavigation()
lcd = LCD_16x2()
prox.update_lights(False)
# nfc = nfc_reader('0x80x', 5)

SHELF_STATE, STATE_IDLE, STATE_PHONE_NOT_DETECTED, STATE_SET_TIMER, STATE_COUNTDOWN, STATE_SESSION_COMPLETE = [i for i in range(0, 6)]

DO_ANIMATION = True
ANIMATION_CYCLE = False
ANIMATION_FRAME_TICK = 0
ANIMATION_UPDATE = True
FRAME_LENGTH = 2

TIME_REMAINING = 6
TIME_INDEX = 5
TIME_LOCK = False
TIME_COMPLETE = False

def lcd_page(page_no):
    global TIME_INDEX
    global TIME_REMAINING
    global ANIMATION_FRAME_TICK
    global ANIMATION_CYCLE
    ANIMATION_FRAME_TICK += 1
    if ANIMATION_FRAME_TICK > FRAME_LENGTH:
        ANIMATION_CYCLE = not ANIMATION_CYCLE
        ANIMATION_FRAME_TICK = 0
    TIME_INDEX = TIME_INDEX
    line_1a,line_2a,line_1b,line_2b = ('Place phone','in shelf','To start','Study session') if page_no == STATE_IDLE else ('Studying...', str(round(TIME_REMAINING/60)), 'Studying...', str(round(TIME_REMAINING/60))) if page_no == STATE_COUNTDOWN else ('Phone not', 'detected', 'Place phone', 'in shelf') if page_no == STATE_PHONE_NOT_DETECTED else ('Set timer', str(TIME_INDEX), 'Set timer', str(TIME_INDEX)) if page_no == STATE_SET_TIMER else ('Session complete', 'Open shelf', 'To start', 'new session') if page_no == STATE_SESSION_COMPLETE else ('error', 'e', 'e', 'error')

    if ANIMATION_CYCLE:
        lcd.display_message(line_1a, line_2=line_2a)
    else:
        lcd.display_message(line_1b, line_2=line_2b)

while True:
    sleep(1)
    if DO_ANIMATION: 
        ANIMATION_FRAME_TICK += 1
    if ANIMATION_FRAME_TICK > FRAME_LENGTH:
        ANIMATION_CYCLE = not ANIMATION_CYCLE 
        ANIMATION_FRAME_TICK = 0
    drawer_closed = prox.is_closed() 
    # phone_placed = nfc.getPhoneState()
    phone_placed = True

    SHELF_STATE = STATE_IDLE if not drawer_closed and not phone_placed else STATE_PHONE_NOT_DETECTED if drawer_closed and not phone_placed else STATE_SET_TIMER if phone_placed and not drawer_closed else STATE_COUNTDOWN if phone_placed and drawer_closed and not TIME_COMPLETE else STATE_SESSION_COMPLETE

    if SHELF_STATE == STATE_COUNTDOWN:
        if not TIME_LOCK:
            TIME_LOCK = True
            TIME_INDEX = TIME_INDEX * 60
            TIME_REMAINING = TIME_INDEX

        TIME_REMAINING -= 1

        if TIME_REMAINING < 1:
            TIME_COMPLETE = True

        prox.update_progress(TIME_REMAINING/TIME_INDEX)

    elif SHELF_STATE == STATE_SET_TIMER:

        if TIME_COMPLETE:
            TIME_COMPLETE = False

        if TIME_LOCK:
            TIME_LOCK = False

        if nav.touch_a1():
            TIME_INDEX += 5

        if nav.touch_a2() and TIME_INDEX >= 5:
            TIME_INDEX -= 5

    lcd_page(SHELF_STATE)
