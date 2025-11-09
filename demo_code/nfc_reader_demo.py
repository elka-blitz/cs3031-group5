# Write your code here :-)
'''
Example: reading NFC tag.
Requires the connection of an NFC reader and the adafruit_pn532 library.
Make sure the circuitpython version you are using is 9.x.
If you need to upgrade, download the version available on the CS3031 canvas page.
Modified version of PN532_simpletest.py. Modified from sample provided by Laura Maye, 2025.
'''

import time
from nfc_reader import nfc_reader 

# known identifier wildcard for phone
identifier_wildcard = '0x80' # this is for a pixel phone. Set to None if wildcard is unknown
# maximum number of false detections in a row before function getPhoneState() returns false
max_false_count = 5
# create an NFC object and initiate connection to reader
nfc_reader = nfc_reader(identifier_wildcard, max_false_count)

while True:
    # Check if a card is available to read

    print(nfc_reader.getPhoneState())
    # Do not respond if no UID is detected
    time.sleep(1)


