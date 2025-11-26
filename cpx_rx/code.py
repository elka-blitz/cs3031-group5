from lcd16x2 import LCD_16x2
from led_controller import led_controller1
from navbuttons import group5StudyAssistantNavigation
from time import sleep
from ir_communicate import ir_shelfstate
from gc import collect

import supervisor
supervisor.runtime.autoreload = False

system_components_connected = True
SHELF_STATE, STATE_IDLE, STATE_PHONE_NOT_DETECTED, STATE_SET_TIMER, STATE_COUNTDOWN, STATE_SESSION_COMPLETE = [i for i in range(0, 6)]
DO_ANIMATION, ANIMATION_CYCLE, ANIMATION_FRAME_TICK, ANIMATION_UPDATE, FRAME_LENGTH  = True, False, 0, True, 2
TIME_REMAINING, TIME_INDEX, TIME_LOCK, TIME_COMPLETE = 6, 1, False, False

try:
    print('lcd')
    lcd = LCD_16x2()
    print('nav')
    nav = group5StudyAssistantNavigation()
    print('led')
    ext_ring_and_prox_sensor = led_controller1()
    print('func')
    ext_ring_and_prox_sensor.update_lights(False)

except Exception:
    print('Components not connected')
    system_components_connected = False

def lcd_page_updater(page_no):
    global TIME_INDEX, TIME_REMAINING, ANIMATION_FRAME_TICK, ANIMATION_CYCLE
    ANIMATION_FRAME_TICK += 1
    if ANIMATION_FRAME_TICK > FRAME_LENGTH:
        ANIMATION_CYCLE = not ANIMATION_CYCLE
        ANIMATION_FRAME_TICK = 0
    TIME_INDEX = TIME_INDEX
    line_1a,line_2a,line_1b,line_2b = ('Place phone','in shelf','To start','Study session') if page_no == STATE_IDLE else ('Studying...', str(round(TIME_REMAINING/60)) + ' minutes', 'Studying...', str(round(TIME_REMAINING/60)) + ' minutes') if page_no == STATE_COUNTDOWN else ('Phone not', 'detected', 'Place phone', 'in shelf') if page_no == STATE_PHONE_NOT_DETECTED else ('Set timer', str(int(TIME_INDEX)) + ' minutes', 'Set timer', str(int(TIME_INDEX)) + ' minutes') if page_no == STATE_SET_TIMER else ('Session complete', 'Open shelf', 'To start', 'new session') if page_no == STATE_SESSION_COMPLETE else ('error', 'e', 'e', 'error')

    if ANIMATION_CYCLE:
        lcd.display_message(line_1a, line_2=line_2a)
    else:
        lcd.display_message(line_1b, line_2=line_2b)



ir = ir_shelfstate()

global_phone_state = False
global_shelf_state = False

while system_components_connected:
    print('\033[96m-----\033[0m')
    print('\033[1mSystem components connected\033[0m')
    sleep(1)
    try:
        received = ir.receive()
        collect()
        if received != None and len(received) == 2:
            print('\033[94mMain process\033[0m', received)
            global_phone_state = received[0]
            global_shelf_state = received[1]

        print('Gobal phone state: ', global_phone_state)
        print('Global shelf state', global_shelf_state)
    except RuntimeError:
        continue

    
    if DO_ANIMATION: 
        ANIMATION_FRAME_TICK += 1
    if ANIMATION_FRAME_TICK > FRAME_LENGTH:
        ANIMATION_CYCLE = not ANIMATION_CYCLE 
        ANIMATION_FRAME_TICK = 0

    drawer_closed = global_shelf_state
    phone_placed = global_phone_state


    print(drawer_closed, phone_placed)

    SHELF_STATE = STATE_IDLE if not drawer_closed and not phone_placed else STATE_PHONE_NOT_DETECTED if drawer_closed and not phone_placed else STATE_SET_TIMER if phone_placed and not drawer_closed else STATE_COUNTDOWN if phone_placed and drawer_closed and not TIME_COMPLETE else STATE_SESSION_COMPLETE

    if SHELF_STATE == STATE_COUNTDOWN:
        if not TIME_LOCK:
            TIME_LOCK = True
            TIME_INDEX = TIME_INDEX * 60
            TIME_REMAINING = TIME_INDEX

        TIME_REMAINING -= 1

        if TIME_REMAINING < 1:
            TIME_COMPLETE = True

        ext_ring_and_prox_sensor.update_progress(TIME_REMAINING/TIME_INDEX)

    elif SHELF_STATE == STATE_SET_TIMER:

        if TIME_COMPLETE:
            TIME_COMPLETE = False

        if TIME_LOCK:
            TIME_LOCK, TIME_INDEX, TIME_REMAINING = False, TIME_INDEX / 60, TIME_REMAINING / 60

        if nav.touch_a1():
            TIME_INDEX += 5

        if nav.touch_a2() and TIME_INDEX >= 10:
            TIME_INDEX -= 5

    lcd_page_updater(SHELF_STATE)
    collect()
while not system_components_connected:
    sleep(1)
    try:
        received = ir.receive()
        if received != None:
            # print('\033[94mMain process\033[0m', received)
            global_phone_state = received[0]
            global_shelf_state = received[1]

        print('Gobal phone state: ', global_phone_state)
        print('Global shelf state', global_shelf_state)
    except RuntimeError:
        continue

    