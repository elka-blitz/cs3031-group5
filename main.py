from create_serial import CreateSerial
import time, os

serial_1 = CreateSerial("/dev/ttyACM0") # creating an instance of the serial connection
serial_1.recordAvailablePorts() # reveal all available ports
serial_1.openPort()  # opens the serial port. Prints a message if this cannot be achieved.

msg = None
run_log = True

t = time.localtime()
date = time.strftime("%Y-%m-%d", t)
clock = time.strftime("%H:%M:%S", t)
filename = f"logs/{date}_log.txt"

try:
    f = open(filename)
    f.write("New logging session initiated\n")
    f.close()
except:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write("date,time,phone_state,shelf_state,system_state_changed,study_time")

got_shelf_state, got_phone_state, got_value = False, False, False
old_phone_state, old_shelf_state = "", ""
got_new_phone_state, got_new_shelf_state = False, False

while run_log:

    try:
        msg = serial_1.readList()
        
        if msg != None:

            for m in msg:
                if "Gobal phone state" in m:
                    msg_split = m.split(" ")
                    phone_state = msg_split[-1]
                    got_phone_state = True
                    if phone_state != old_phone_state:
                        got_new_phone_state = True
                        old_phone_state = phone_state

                elif "Global shelf state" in m:
                    msg_split = m.split(" ")
                    shelf_state = msg_split[-1]
                    got_shelf_state = True
                    if shelf_state != old_shelf_state:
                        got_new_shelf_state = True
                        old_shelf_state = shelf_state

                elif "Value" in m:
                    msg_split = m.split(" ")
                    value = msg_split[1] 
                    got_value = True

            if (got_shelf_state and got_phone_state and got_value):
                system_state_changed = (got_new_phone_state or got_new_shelf_state)
                with open(filename, "a") as f:
                    f.write(f"{date},{clock},{phone_state},{shelf_state},{str(system_state_changed)}{value}\n")
                got_shelf_state = got_phone_state = got_value = got_new_phone_state = got_new_shelf_state = False

    except IndexError:
        pass

    time.sleep(0.5)
serial_1.close()