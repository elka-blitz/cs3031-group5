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
    f.close()
except:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write("New logging session initiated\n")

while run_log:
    try:
        msg = serial_1.readList()
        
        if msg != None:

            for m in msg:
                if "Gobal phone state" in m:
                    msg_split = m.split(" ")
                    phone_state = msg_split[-1]
                if "Global shelf state" in m:
                    msg_split = m.split(" ")
                    shelf_state = msg_split[-1]
                if "Value" in m:
                    msg_split = m.split(" ")
                    value = m.split(1) 

            with open(filename, "a") as f:
                f.write(f"{date},{clock},{"Phone:"},{phone_state},{"Shelf:"},{shelf_state},{"Value:"},{value}\n")
    except IndexError:
        pass

    time.sleep(0.5)
serial_1.close()