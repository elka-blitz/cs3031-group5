from busio import UART
from board import TX, RX
from adafruit_pn532 import PN532_UART

def uid_string(uid):
    return ''.join([hex(i) for i in uid])

class nfc_reader:

    def __init__(self, identifier_wildcard, max_check_count):       
        self._uart = UART(TX, RX, baudrate=115200, timeout=0.1)
        self._pn532 = PN532_UART(self._uart , debug=False)
        self._pn532.SAM_configuration()
        self.recent_checks = []
        self.identifier_wildcard = identifier_wildcard
        self.max_check_count = max_check_count

    def read(self):
        uid = self._pn532.read_passive_target(timeout=0.1)

        if uid == None:
            return ["0x00"]
        
        if type(uid) is bytes:
            uid = [uid]

        uid_string_array = [uid_string(i) for i in uid]
        return uid_string_array
        
    def poweroff(self):
        self._pn532.power_down()

    def getPhoneState(self):
        found_phone = False

        if len(self.recent_checks) > self.max_check_count:
            self.recent_checks.pop(0)

        try:
            uid_array = self.read()
            self.recent_checks += uid_array
            
        except RuntimeError:
            print("Skipping read.")

        unique_uid = set(self.recent_checks)

        if self.identifier_wildcard == None:
            prefix_uid = [uuid[:4] for uuid in unique_uid]
            if len(set(prefix_uid)) != len(prefix_uid):
                found_phone = True
        else:
            for uuid in unique_uid:
                if self.identifier_wildcard != uuid[:4]:
                    unique_uid.remove(uuid)
            if len(unique_uid) > 1:
                found_phone = True
        
        self.poweroff()
        return found_phone