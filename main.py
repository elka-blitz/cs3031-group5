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
        f.write("date,time,phone_state,shelf_state,study_time")

new_shelf_state, new_phone_state, new_value = False, False, False

while run_log:

    try:
        msg = serial_1.readList()
        
        if msg != None:

            for m in msg:
                if "Gobal phone state" in m:
                    msg_split = m.split(" ")
                    phone_state = msg_split[-1]
                    new_phone_state = True

                elif "Global shelf state" in m:
                    msg_split = m.split(" ")
                    shelf_state = msg_split[-1]
                    new_shelf_state = True

                elif "Value" in m:
                    msg_split = m.split(" ")
                    value = msg_split[1] 
                    new_value = True

            if (new_shelf_state and new_phone_state and new_value):
                with open(filename, "a") as f:
                    f.write(f"{date},{clock},{phone_state},{shelf_state},{value}\n")
                new_shelf_state, new_phone_state, new_value = False, False, False

    except IndexError:
        pass

    time.sleep(0.5)
serial_1.close()