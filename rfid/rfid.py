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

        # Configure PN532 to communicate with MiFare cards
        self.pn532.SAM_configuration()

        self.uid = 0
        self.card_dict = {
            '734a266f': False,
            '5d81e96d': False,
            '4d71f56d': False,
            'fdd1a46b': False,
            '1d4ba46b': False,
            'dd8b9f6b': False
        }

    def output_uid(self):
        print("Waiting for RFID/NFC card...")
        while True:
            # Check if a card is available to read
            self.uid = self.pn532.read_passive_target(timeout=0.5)
            print(".", end="")
            # Try again if no card is available.
            if self.uid is None:
                continue
            print("Found card with UID:", [hex(i) for i in self.uid])

    def set_uid(self, uid):
        self.uid = uid

    def get_uid(self):
        return self.uid

    def scan_card(self):
        self.uid = None

        while self.uid is None:
            self.uid = self.pn532.read_passive_target(timeout=0.5)

        uid = [hex(i) for i in self.uid]
        self.uid = ""

        for string in uid:
            self.uid += string[2:]

        for uid in self.card_dict:
            if uid == self.uid:
                self.card_dict[uid] = True

    def scan_card_remove(self):
        self.uid = None

        while self.uid is None:
            self.uid = self.pn532.read_passive_target(timeout=0.5)

        uid = [hex(i) for i in self.uid]
        self.uid = ""

        for string in uid:
            self.uid += string[2:]

        for uid in self.card_dict:
            if uid == self.uid:
                self.card_dict[uid] = False

    def check_registration(self):
        for uid in self.card_dict:
            if uid == self.uid:
                return self.card_dict[uid]


if __name__ == "__main__":
    rfid = RFID()
