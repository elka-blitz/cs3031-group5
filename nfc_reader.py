import time, busio, board
from adafruit_pn532.uart import PN532_UART

# method to convert UID address to a string
def uid_string(uid):
    return ''.join([hex(i) for i in uid])

class nfc_reader:

    def __init__(self, identifier_wildcard, false_count):
        # UART connection
        self._uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0.1)
        self._pn532 = PN532_UART(self._uart , debug=False)
        ic, ver, rev, support = self._pn532.firmware_version
        print(f"Found PN532 with firmware version: {ver}.{rev}")
        self._pn532.SAM_configuration()
        self.recent_checks = []
        self.identifier_wildcard = identifier_wildcard
        self.max_false_count = max_false_count

    def read(self):
        uid = self._pn532.read_passive_target(timeout=0.1)
        return uid

    def poweroff(self):
        self._pn532.power_down()

    def getPhoneState(self,identifier_wildcard):
        found_phone = False
        uid = self.read()
        
        if uid != None:
            uid_str = uid_string(uid)
            self.recent_checks.append(uid_str)
        else:
            self.recent_checks.append(str(uid))
        
        for check in self.recent_checks:
            if self.identifier_wildcard in check:
                found_phone = True

        if len(self.recent_checks) > self.max_false_count:
            self.recent_checks.pop(0)
            print(self.recent_checks)
        
        self.poweroff()
        return found_phone
