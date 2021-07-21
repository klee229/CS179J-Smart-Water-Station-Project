# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI


class RFID:

    def __init__(self):
        self.reset_pin = DigitalInOut(board.D6)
        self.req_pin = DigitalInOut(board.D12)

        # SPI connection:
        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.cs_pin = DigitalInOut(board.D5)
        self.pn532 = PN532_SPI(self.spi, self.cs_pin, debug=False)
        self.ic, self.ver, self.rev, self.support = self.pn532.firmware_version
        print("Found PN532 with firmware version: {0}.{1}".format(self.ver, self.rev))

        # Configure PN532 to communicate with MiFare cards
        self.pn532.SAM_configuration()

        self.uid = 0

    def get_uid(self):
        print("Waiting for RFID/NFC card...")
        while True:
            # Check if a card is available to read
            self.uid = self.pn532.read_passive_target(timeout=0.5)
            print(".", end="")
            # Try again if no card is available.
            if self.uid is None:
                continue
            print("Found card with UID:", [hex(i) for i in self.uid])


if __name__ == '__main__':
    rfid = RFID()
    rfid.get_uid()
