'''
Serial class for receiving circuit python data
Class was compiled for the module CS2013
by Laura Maye (2021).
Note, this class is not official! There may be several bugs as it is still in testing!
If you find any issues with the class, feel free to contact me about suggested changes.
You may also make such changes yourself, or extend on the class if you like.
'''

import serial
import serial.tools.list_ports

class CreateSerial: # class for creating and reading serial data.

    __ports_available = []

    # init function, used to create an instance of the CreateSerial class
    def __init__(self, port=None):
        self.__ser = serial.Serial()
        self.__ser.baud_rate = 9600
        self.__ser.port = port
        self.recordAvailablePorts()

    # used to keep a record of all Serial ports available. Updates for all instances.
    def recordAvailablePorts(self):
        ports = serial.tools.list_ports.comports()
        CreateSerial.__ports_available = [str(port).split("-")[0].replace(" ", "") for port in ports]
        print("\n---------SERIAL PORTS AVAILABLE: BEGIN--------------")
        print(*CreateSerial.__ports_available, sep="\n")
        print("---------SERIAL PORTS AVAILABLE: END----------------\n")

    # open the Serial port. Prints an error message and terminates the program if not possible.
    def openPort(self):
        if self.__ser.name not in CreateSerial.__ports_available:
            print("Port '%s' is not available. Check the following:" % str(self.__ser.port))
            print("Is the device connected? See available ports by calling recordAvailablePorts().")
            print("Is there a typo in the device name? See available ports by calling recordAvailablePorts().")
            quit()
        else:
            try:
                self.__ser.open()
                print("Port '%s' has opened successfully." % str(self.__ser.port))
            except serial.SerialException:
                print("Resource busy! Is the serial monitor still running in mu-editor?")
                quit()

    # check if the serial port is already open.
    def checkOpen(self):
        return self.__ser.is_open

    # set the port
    def setPort(self, port):
        self.__ser.port = port

    # get the port. Returns string representation of port.
    def getPort(self):
        return str(self.__ser.port)

    #set baud rate for Serial connection
    def setBaudRate(self, new_baud):
        self.__ser.baud_rate = new_baud

    #get baud rate. Returns string representation of baud rate.
    def getBaudRate(self):
        return str(self.__ser.baud_rate)

    # this function reads in serial data if there is data in waiting.
    # returns the data as a string list, with a key:value
    # note: you should not call both readList() and readDictionary() in the same loop.
    def readList(self):
        data_received = ""
        returned_data = []
        while self.__ser.in_waiting:
            data_received = self.__ser.readline().decode('utf-8')
            returned_data.append(data_received.split("\n")[0][:-1])
        if returned_data != []:
            return returned_data
        return None

    # this function reads in serial data if there is data in waiting.
    # returns the data as a dictionary, with a key:value
    # note: you should not call both readList() and readDictionary() in the same loop.
    def readDictionary(self):
        data_received = ""
        returned_data = {}
        while self.__ser.in_waiting:
            data_received = self.__ser.readline().decode('utf-8')
            key_value = data_received.split(": ")
            key_value[1] = key_value[1].strip()
            try:
                key_value[1] = float(key_value[1])
            except:
                pass
            returned_data[key_value[0]] = key_value[1]
        if returned_data != {}:
            return returned_data
        return None
    
    def convertDictionary(self, data_received):
        returned_data = {}
        key_value = data_received.split(": ")
        key_value[1] = key_value[1].strip()
        try:
            key_value[1] = float(key_value[1])
        except:
            pass
        returned_data[key_value[0]] = key_value[1]
        if returned_data != {}:
            return returned_data
        return None



    def read_test(self):
        data_received = ""
        returned_data = {}
        while self.__ser.in_waiting > 0:
            incoming = self.__ser.read(1)
            if incoming != b'\r':
                data_received += incoming.decode("utf-8")
            elif incoming == b'\r':
                break
        if data_received != "":
            converted = self.convertDictionary(data_received)
            if converted != None:
                return converted
    
    def write(self, data):
        self.__ser.write(str.encode(data))

    # close the serial port.
    def close(self):
        if not self.checkOpen():
            self.__ser.close()

    