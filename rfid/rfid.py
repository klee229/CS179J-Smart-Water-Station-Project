# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
import pandas as pd


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

        # NOTE: enter the exact path for your machine to run locally
        self.file_path = ''
        self.uid = ''

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

    def get_uid(self):
        return self.uid

    def scan_card(self):
        self.uid = None

        while self.uid is None:
            self.uid = self.pn532.read_passive_target(timeout=0.5)

        uid = [hex(i) for i in self.uid]
        self.uid = ''

        for string in uid:
            self.uid += string[2:]

    def register_card(self, the_uid):
        df = pd.read_csv(self.file_path)

        index = df.index[df['card_uid'] == the_uid].tolist()

        card_state = df.at[index[0], 'registration_state']

        if not card_state:
            df.at[index[0], 'registration_state'] = True
            df.to_csv(self.file_path, index=False)

    def unregister_card(self, the_uid):
        self.uid = ''

        df = pd.read_csv(self.file_path)

        index = df.index[df['card_uid'] == the_uid].tolist()

        card_state = df.at[index[0], 'registration_state']

        if card_state:
            df.at[index[0], 'registration_state'] = False
            df.to_csv(self.file_path, index=False)

    def check_registration(self, the_uid):
        df = pd.read_csv(self.file_path)

        index = df.index[df['card_uid'] == the_uid].tolist()

        if len(index) is not 0:
            card_state = df.at[index[0], 'registration_state']
        else:
            card_state = False

        return card_state


if __name__ == '__main__':
    rfid = RFID()
    
