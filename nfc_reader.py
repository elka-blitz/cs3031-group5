from busio import UART
from board import TX, RX
from adafruit_pn532 import PN532_UART

def uid_string(uid):
    return ''.join([hex(i) for i in uid])

class nfc_reader:

    def __init__(self, identifier_wildcard, exclusion_ids, max_check_count):       
        self._uart = UART(TX, RX, baudrate=115200, timeout=0.1)
        self._pn532 = PN532_UART(self._uart , debug=False)
        self._pn532.SAM_configuration()
        self.recent_checks = []
        self.identifier_wildcard = identifier_wildcard
        if identifier_wildcard != None:
            self.len_wildcard = len(identifier_wildcard)
        self.exclusion_ids = exclusion_ids
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
            for uid in uid_array:
                if uid in self.exclusion_ids:
                    uid_array.remove(uid)
            self.recent_checks += uid_array
            
        except RuntimeError:
            print("Skipping read.")

        unique_uid = set(self.recent_checks)

        if self.identifier_wildcard == None:
            prefix_uid = [a[:5] for a in unique_uid]
            unique_prefix_uid = set(prefix_uid)
            [prefix_uid.remove(b) for b in unique_prefix_uid]
            for j in prefix_uid:
                valid_detections = [c for c in unique_uid if c[:5] == prefix_uid]
                uid_lengths = [len(d) for d in valid_detections]
                found_phone = True
        else:
            valid_detections = [i for i in unique_uid if i[:self.len_wildcard] == self.identifier_wildcard]
            if len(valid_detections) > 1:
                uid_lengths = [len(j) for j in valid_detections]
                if len(set(uid_lengths)) > uid_lengths:
                    found_phone = True
        
        self.poweroff()
        return found_phone