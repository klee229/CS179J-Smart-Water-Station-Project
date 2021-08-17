import unittest
import csv
import os

from rfid.rfid_no_hardware import RFIDNoHardware


class TestRFIDClass(unittest.TestCase):

    # NOTE: enter the exact path for your machine to run locally
    path = ''

    def create_test_file(self):
        self.file_path = TestRFIDClass.path

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        columns = ['card_uid', 'registration_state', 'name', 'age', 'sex', 'activity_level',
                   'daily_hydration_lower', 'daily_hydration_upper', 'water_dispensed', 'total_dispensed',
                   'percent_dispensed_of_daily', 'num_days', 'num_days_goal', 'avg_intake', 'last_login'
                   ]

        user_data = [
            ['734a266f', False, ' ', 0, ' ', ' ', 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, ' '],
            ['5d81e96d', False, ' ', 0, ' ', ' ', 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, ' '],
            ['4d71f56d', False, ' ', 0, ' ', ' ', 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, ' '],
            ['fdd1a46b', False, ' ', 0, ' ', ' ', 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, ' '],
            ['1d4ba46b', False, ' ', 0, ' ', ' ', 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, ' '],
            ['dd8b9f6b', False, ' ', 0, ' ', ' ', 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, ' ']
        ]

        # open file, write data to file
        with open(self.file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(user_data)

        csv_file.close()

    def delete_test_file(self):
        self.file_path = TestRFIDClass.path

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_set_get_uid(self):
        card_uids = ['734a266f', '5d81e96d', '4d71f56d', 'fdd1a46b', '1d4ba46b', 'dd8b9f6b']

        rfid = RFIDNoHardware()

        for uid in card_uids:
            rfid.set_uid(uid)
            self.assertEqual(uid, rfid.get_uid())

    def test_register_card(self):
        card_uids = ['734a266f', '5d81e96d', '4d71f56d', 'fdd1a46b', '1d4ba46b', 'dd8b9f6b']

        rfid = RFIDNoHardware()

        self.create_test_file()

        for uid in card_uids:
            rfid.register_card(uid)
            self.assertEqual(True, rfid.check_registration(uid))

        self.delete_test_file()

    def test_unregister_card(self):
        card_uids = ['734a266f', '5d81e96d', '4d71f56d', 'fdd1a46b', '1d4ba46b', 'dd8b9f6b']

        rfid = RFIDNoHardware()

        self.create_test_file()

        for uid in card_uids:
            rfid.unregister_card(uid)
            self.assertEqual(False, rfid.check_registration(uid))

        self.delete_test_file()


if __name__ == '__main__':
    unittest.main()
