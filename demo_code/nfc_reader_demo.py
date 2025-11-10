# Write your code here :-)
'''
Example: reading NFC tag.
Requires the connection of an NFC reader and the adafruit_pn532 library.
Make sure the circuitpython version you are using is 9.x.
If you need to upgrade, download the version available on the CS3031 canvas page.
Modified version of PN532_simpletest.py. Modified from sample provided by Laura Maye, 2025.

Modified adfruit_pn532 library ONLY SUPPORTS UART. Wire PN532 TX <-> circuitpython RX.
Function getPhoneState is not described in code to save memory. The function will return True once a phone is detected.
For a known wildcard identifier, the function will return true if multiple different strings are detected beginning with the same wildcard.
This ensures that phone presence is detected despite rotating identifiers - the first byte is observed to be static.
If no identifier is known, None can be passed instead.
The function will compare the list of unique wildcards and identifiers, and return True if there are fewer wildcards.
This is less reliable as it could trigger on two different tags which share a similar identifier.
'''

import time
from nfc_reader import nfc_reader 

# known identifier wildcard for phone
identifier_wildcard = '0x80x' # this is for a pixel phone. Set to None if wildcard is unknown
# maximum number of false detections in a row before function getPhoneState() returns false
max_false_count = 5
exclusion_ids = []
# create an NFC object and initiate connection to reader
nfc_reader = nfc_reader(identifier_wildcard, exclusion_ids, max_false_count)

while True:
    # Check if a card is available to read

    print(nfc_reader.getPhoneState())
    # Do not respond if no UID is detected
    time.sleep(1)


