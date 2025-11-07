# SPDX-FileCopyrightText: 2015-2018 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
``adafruit_pn532``
====================================================

This module will let you communicate with a PN532 RFID/NFC shield or breakout
using I2C, SPI or UART.

* Author(s): Original Raspberry Pi code by Tony DiCola, CircuitPython by ladyada

Implementation Notes
--------------------

**Hardware:**

* Adafruit `PN532 Breakout <https://www.adafruit.com/product/364>`_
* Adafruit `PN532 Shield <https://www.adafruit.com/product/789>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time

from digitalio import Direction
from micropython import const

try:
    from typing import Optional, Tuple, Union
    from busio import UART
    from circuitpython_typing import ReadableBuffer
    from digitalio import DigitalInOut
except ImportError:
    pass

__version__ = "2.4.6"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PN532.git"

_PREAMBLE = const(0x00)
_STARTCODE1 = const(0x00)
_STARTCODE2 = const(0xFF)
_POSTAMBLE = const(0x00)

_HOSTTOPN532 = const(0xD4)
_PN532TOHOST = const(0xD5)

# PN532 Commands
_COMMAND_GETFIRMWAREVERSION = const(0x02)
_COMMAND_SAMCONFIGURATION = const(0x14)
_COMMAND_POWERDOWN = const(0x16)
_COMMAND_INLISTPASSIVETARGET = const(0x4A)

_MIFARE_ISO14443A = const(0x00)

# Mifare Commands
MIFARE_CMD_AUTH_A = const(0x60)
MIFARE_CMD_AUTH_B = const(0x61)
MIFARE_CMD_READ = const(0x30)
MIFARE_CMD_WRITE = const(0xA0)
MIFARE_CMD_TRANSFER = const(0xB0)
MIFARE_CMD_DECREMENT = const(0xC0)
MIFARE_CMD_INCREMENT = const(0xC1)
MIFARE_CMD_STORE = const(0xC2)
MIFARE_ULTRALIGHT_CMD_WRITE = const(0xA2)

_ACK = b"\x00\x00\xff\x00\xff\x00"

class BusyError(Exception):
    """Base class for exceptions in this module."""


class PN532_UART:
    """PN532 driver base, must be extended for I2C/SPI/UART interfacing"""

    def __init__(
        self,
        uart: UART,
        *,
        debug: bool = False,
        irq: Optional[DigitalInOut] = None,
        reset: Optional[DigitalInOut] = None,
    ) -> None:
        """Create an instance of the PN532 class"""
        self.low_power = True
        self._uart = uart
        self.debug = debug
        self._irq = irq
        self._reset_pin = reset
        self.reset()
        _ = self.firmware_version

    def _read_data(self, count: int) -> bytes: # previously Union[bytes, bytearray]
        """Read a specified count of bytes from the PN532."""
        frame = self._uart.read(count)
        if not frame:
            raise BusyError("No data read from PN532")
        if self.debug:
            print("Reading: ", [hex(i) for i in frame])
        return frame

    def _write_data(self, framebytes: bytes) -> None:
        """Write a specified count of bytes to the PN532"""
        self._uart.reset_input_buffer()
        self._uart.write(framebytes)

    def _wait_ready(self, timeout: float) -> bool:
        """Wait `timeout` seconds"""
        timestamp = time.monotonic()
        while (time.monotonic() - timestamp) < timeout:
            if self._uart.in_waiting > 0:
                return True  # No Longer Busy
            time.sleep(0.01)  # lets ask again soon!
        # Timed out!
        return False

    def _wakeup(self) -> None:
        """Send any special commands/data to wake up PN532"""
        if self._reset_pin:
            self._reset_pin.value = True
            time.sleep(0.01)
        self.low_power = False
        self._uart.write(
            b"\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )  # wake up!
        self.SAM_configuration()


    def reset(self) -> None:
        """Perform a hardware reset toggle and then wake up the PN532"""
        if self._reset_pin:
            if self.debug:
                print("Resetting")
            self._reset_pin.direction = Direction.OUTPUT
            self._reset_pin.value = False
            time.sleep(0.1)
            self._reset_pin.value = True
            time.sleep(0.1)
        self._wakeup()

    def _write_frame(self, data: bytearray) -> None:
        """Write a frame to the PN532 with the specified data bytearray."""
        assert data is not None and 1 < len(data) < 255, "Data must be array of 1 to 255 bytes."
        # Build frame to send as:
        # - Preamble (0x00)
        # - Start code  (0x00, 0xFF)
        # - Command length (1 byte)
        # - Command length checksum
        # - Command bytes
        # - Checksum
        # - Postamble (0x00)
        length = len(data)
        frame = bytearray(length + 8)
        frame[0] = _PREAMBLE
        frame[1] = _STARTCODE1
        frame[2] = _STARTCODE2
        checksum = sum(frame[0:3])
        frame[3] = length & 0xFF
        frame[4] = (~length + 1) & 0xFF
        frame[5:-2] = data
        checksum += sum(data)
        frame[-2] = ~checksum & 0xFF
        frame[-1] = _POSTAMBLE
        # Send frame.
        if self.debug:
            print("Write frame: ", [hex(i) for i in frame])
        self._write_data(bytes(frame))

    def _read_frame(self, length: int) -> Union[bytes, bytearray]:
        """Read a response frame from the PN532 of at most length bytes in size.
        Returns the data inside the frame if found, otherwise raises an exception
        if there is an error parsing the frame.  Note that less than length bytes
        might be returned!
        """
        # Read frame with expected length of data.
        response = self._read_data(length + 7)
        if self.debug:
            print("Read frame:", [hex(i) for i in response])

        # Swallow all the 0x00 values that preceed 0xFF.
        offset = 0
        while response[offset] == 0x00:
            offset += 1
            if offset >= len(response):
                raise RuntimeError("Response frame preamble does not contain 0x00FF!")
        if response[offset] != 0xFF:
            raise RuntimeError("Response frame preamble does not contain 0x00FF!")
        offset += 1
        if offset >= len(response):
            raise RuntimeError("Response contains no data!")
        # Check length & length checksum match.
        frame_len = response[offset]
        if (frame_len + response[offset + 1]) & 0xFF != 0:
            raise RuntimeError("Response length checksum did not match length!")
        # Check frame checksum value matches bytes.
        checksum = sum(response[offset + 2 : offset + 2 + frame_len + 1]) & 0xFF
        if checksum != 0:
            raise RuntimeError("Response checksum did not match expected value: ", checksum)
        # Return frame data.
        return response[offset + 2 : offset + 2 + frame_len]

    def call_function(
        self,
        command: int,
        response_length: int = 0,
        params: ReadableBuffer = b"",
        timeout: float = 1,
    ) -> Optional[Union[bytes, bytearray]]:
        """Send specified command to the PN532 and expect up to response_length
        bytes back in a response.  Note that less than the expected bytes might
        be returned!  Params can optionally specify an array of bytes to send as
        parameters to the function call.  Will wait up to timeout seconds
        for a response and return a bytearray of response bytes, or None if no
        response is available within the timeout.
        """
        if not self.send_command(command, params=params, timeout=timeout):
            return None
        return self.process_response(command, response_length=response_length, timeout=timeout)

    def send_command(self, command: int, params: ReadableBuffer = b"", timeout: float = 1) -> bool:
        """Send specified command to the PN532 and wait for an acknowledgment.
        Will wait up to timeout seconds for the acknowledgment and return True.
        If no acknowledgment is received, False is returned.
        """
        if self.low_power:
            self._wakeup()

        # Build frame data with command and parameters.
        data = bytearray(2 + len(params))
        data[0] = _HOSTTOPN532
        data[1] = command & 0xFF
        for i, val in enumerate(params):
            data[2 + i] = val
        # Send frame and wait for response.
        try:
            self._write_frame(data)
        except OSError:
            return False
        if not self._wait_ready(timeout):
            return False
        # Verify ACK response and wait to be ready for function response.
        if not _ACK == self._read_data(len(_ACK)):
            raise RuntimeError("Did not receive expected ACK from PN532!")
        return True

    def process_response(
        self, command: int, response_length: int = 0, timeout: float = 1
    ) -> Optional[Union[bytes, bytearray]]:
        """Process the response from the PN532 and expect up to response_length
        bytes back in a response.  Note that less than the expected bytes might
        be returned! Will wait up to timeout seconds for a response and return
        a bytearray of response bytes, or None if no response is available
        within the timeout.
        """
        if not self._wait_ready(timeout):
            return None
        # Read response bytes.
        response = self._read_frame(response_length + 2)
        # Check that response is for the called function.
        if not (response[0] == _PN532TOHOST and response[1] == (command + 1)):
            raise RuntimeError("Received unexpected command response!")
        # Return response data.
        return response[2:]

    def power_down(self) -> bool:
        """Put the PN532 into a low power state. If the reset pin is connected a
        hard power down is performed, if not, a soft power down is performed
        instead. Returns True if the PN532 was powered down successfully or
        False if not."""
        if self._reset_pin:  # Hard Power Down if the reset pin is connected
            self._reset_pin.value = False
            self.low_power = True
        else:
            # Soft Power Down otherwise. Enable wakeup on I2C, SPI, UART
            response = self.call_function(_COMMAND_POWERDOWN, params=[0xB0, 0x00])
            self.low_power = response[0] == 0x00
        time.sleep(0.005)
        return self.low_power

    @property
    def firmware_version(self) -> Tuple[int, int, int, int]:
        """Call PN532 GetFirmwareVersion function and return a tuple with the IC,
        Ver, Rev, and Support values.
        """
        response = self.call_function(_COMMAND_GETFIRMWAREVERSION, 4, timeout=0.5)
        if response is None:
            raise RuntimeError("Failed to detect the PN532")
        return tuple(response)

    def SAM_configuration(self) -> None:
        """Configure the PN532 to read MiFare cards."""
        # Send SAM configuration command with configuration for:
        # - 0x01, normal mode
        # - 0x14, timeout 50ms * 20 = 1 second
        # - 0x01, use IRQ pin
        # Note that no other verification is necessary as call_function will
        # check the command was executed as expected.
        self.call_function(_COMMAND_SAMCONFIGURATION, params=[0x01, 0x14, 0x01])

    def read_passive_target(
        self, card_baud: int = _MIFARE_ISO14443A, timeout: float = 1
    ) -> Optional[bytearray]:
        """Wait for a MiFare card to be available and return its UID when found.
        Will wait up to timeout seconds and return None if no card is found,
        otherwise a bytearray with the UID of the found card is returned.
        """
        # Send passive read command for 1 card.  Expect at most a 7 byte UUID.
        response = self.listen_for_passive_target(card_baud=card_baud, timeout=timeout)
        # If no response is available return None to indicate no card is present.
        if not response:
            return None
        return self.get_passive_target(timeout=timeout)

    def listen_for_passive_target(
        self, card_baud: int = _MIFARE_ISO14443A, timeout: float = 1
    ) -> bool:
        """Send command to PN532 to begin listening for a Mifare card. This
        returns True if the command was received successfully. Note, this does
        not also return the UID of a card! `get_passive_target` must be called
        to read the UID when a card is found. If just looking to see if a card
        is currently present use `read_passive_target` instead.
        """
        # Send passive read command for 1 card.  Expect at most a 7 byte UUID.
        try:
            response = self.send_command(
                _COMMAND_INLISTPASSIVETARGET, params=[0x01, card_baud], timeout=timeout
            )
        except BusyError:
            return False  # _COMMAND_INLISTPASSIVETARGET failed
        return response

    def get_passive_target(self, timeout: float = 1) -> Optional[Union[bytes, bytearray]]:
        """Will wait up to timeout seconds and return None if no card is found,
        otherwise a bytearray with the UID of the found card is returned.
        `listen_for_passive_target` must have been called first in order to put
        the PN532 into a listening mode.

        It can be useful to use this when using the IRQ pin. Use the IRQ pin to
        detect when a card is present and then call this function to read the
        card's UID. This reduces the amount of time spend checking for a card.
        """
        response = self.process_response(
            _COMMAND_INLISTPASSIVETARGET, response_length=30, timeout=timeout
        )
        # If no response is available return None to indicate no card is present.
        if response is None:
            return None
        # Check only 1 card with up to a 7 byte UID is present.
        if response[0] != 0x01:
            raise RuntimeError("More than one card detected!")
        if response[5] > 7:
            raise RuntimeError("Found card with unexpectedly long UID!")
        # Return UID of card.
        return response[6 : 6 + response[5]]