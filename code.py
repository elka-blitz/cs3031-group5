from lcd16x2 import LCD_16x2
from time import sleep
from led_controller import led_controller
from navbuttons import group5StudyAssistantNavigation
from time import sleep, time
from adafruit_circuitplayground import cp

prox = led_controller()
nav = group5StudyAssistantNavigation()
lcd = LCD_16x2()
prox.update_lights(False)
# nfc = nfc_reader('0x80x', 5)

SHELF_STATE, STATE_IDLE, STATE_PHONE_NOT_DETECTED, STATE_SET_TIMER, STATE_COUNTDOWN = [i for i in range(0, 5)]

DO_ANIMATION = True
ANIMATION_CYCLE = False
ANIMATION_FRAME_TICK = 0
ANIMATION_UPDATE = True
FRAME_LENGTH = 2

TIME_REMAINING = 100
TIME_INDEX = ''

def lcd_page(page_no):
    global TIME_REMAINING
    global ANIMATION_FRAME_TICK
    global ANIMATION_CYCLE
    ANIMATION_FRAME_TICK += 1
    if ANIMATION_FRAME_TICK > FRAME_LENGTH:
        ANIMATION_CYCLE = not ANIMATION_CYCLE
        ANIMATION_FRAME_TICK = 0

    line_1a,line_2a,line_1b,line_2b = ('Place phone','in shelf','To start','Study session') if page_no == STATE_IDLE else ('Studying...', str(TIME_REMAINING), 'Studying...', str(TIME_REMAINING)) if page_no == STATE_COUNTDOWN else ('Phone not', 'detected', 'Place phone', 'in shelf') if page_no == STATE_PHONE_NOT_DETECTED else ('Set timer', TIME_INDEX, 'Set timer', TIME_INDEX) if page_no == STATE_SET_TIMER else ('error', 'e', 'e', 'error')

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
    phone_placed = cp.switch

    SHELF_STATE = STATE_IDLE if not drawer_closed and not phone_placed else STATE_PHONE_NOT_DETECTED if drawer_closed and not phone_placed else STATE_SET_TIMER if phone_placed and not drawer_closed else STATE_COUNTDOWN if phone_placed and drawer_closed else 'error'
    
    lcd_page(SHELF_STATE)

    if SHELF_STATE == STATE_COUNTDOWN:
        TIME_REMAINING -= 1

    elif SHELF_STATE == STATE_SET_TIMER:
        if nav.touch_a1():
            TIME_INDEX += 1
        if nav.touch_a2():
            TIME_INDEX -= 1
    else:
        print('error')