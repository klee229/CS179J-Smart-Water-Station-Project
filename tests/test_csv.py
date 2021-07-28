import unittest
import csv
import pandas as pd


class TestCSVFile(unittest.TestCase):

    def test_open_write_read_close(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'gender', 'age', 'activity_level', 'daily_hydration',
                   'num_days', 'num_days_goal', 'water_dispensed', 'avg_intake']
        user_data = [
            ['734a266f', 'True', 'Chris Smith', 'Female', '42', 'Sedentary', '2000', '100', '99', '214503', '2145.03'],
            ['5d81e96d', 'True', 'Ivann Cruz', 'Male', '81', 'Active', '2200-2400', '365', '157', '725604', '1987.96'],
            ['4a273b9e', 'True', 'Ken Lee', 'Male', '4', 'Moderate', '1400-1600', '10', '3', '13045', '1304.5']
        ]

        # NOTE: enter the exact path for your machine to run locally
        path = ''

        # open file, write data to file
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(user_data)

        # open file, read data from file
        with open(path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_num = 0
            for row in reader:
                if row_num == 0:
                    self.assertEqual(columns, row)
                else:
                    self.assertEqual(user_data[row_num-1], row)
                row_num += 1

        csv_file.close()

    def test_reopen_read_close(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'gender', 'age', 'activity_level', 'daily_hydration',
                   'num_days', 'num_days_goal', 'water_dispensed', 'avg_intake']
        user_data = [
            ['734a266f', 'True', 'Chris Smith', 'Female', '42', 'Sedentary', '2000', '100', '99', '214503', '2145.03'],
            ['5d81e96d', 'True', 'Ivann Cruz', 'Male', '81', 'Active', '2200-2400', '365', '157', '725604', '1987.96'],
            ['4a273b9e', 'True', 'Ken Lee', 'Male', '4', 'Moderate', '1400-1600', '10', '3', '13045', '1304.5']
        ]

        # NOTE: enter the exact path for your machine to run locally
        path = ''

        # open file, read data from file
        with open(path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_num = 0
            for row in reader:
                if row_num == 0:
                    self.assertEqual(columns, row)
                else:
                    self.assertEqual(user_data[row_num - 1], row)
                row_num += 1

        csv_file.close()

    def test_add_row(self):
        # example user for testing
        example_user = ['Test User', 'Female', '100', 'Active', '2000', '100', '100', '200000', '2000', '1a2b3c4d']

        # NOTE: enter the exact path for your machine to run locally
        path = ''

        # open file in append mode, write data to end of file
        with open(path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(example_user)

        # open file, read data from file
        with open(path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            new_row = []
            for row in reader:
                if row[0] == example_user[0]:
                    new_row = row

        self.assertEqual(example_user, new_row)

        csv_file.close()

    def test_edit_user_data(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'gender', 'age', 'activity_level', 'daily_hydration',
                   'num_days', 'num_days_goal', 'water_dispensed', 'avg_intake']
        user_data = [
            ['734a266f', 'True', 'Chris Smith', 'Female', '42', 'Sedentary', '2000', '100', '99', '214503', '2145.03'],
            ['5d81e96d', 'True', 'Ivann Cruz', 'Male', '81', 'Active', '2200-2400', '365', '157', '725604', '1987.96'],
            ['4a273b9e', 'True', 'Ken Lee', 'Male', '4', 'Moderate', '1400-1600', '10', '3', '13045', '1304.5']
        ]

        # NOTE: enter the exact path for your machine to run locally
        path = ''

        # open file, write data to file
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(user_data)

        row_to_change = 0

        # open file, read data from file
        with open(path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_num = 0
            for row in reader:
                if row[0] == '734a266f':
                    row_to_change = row_num
                row_num += 1

        # create pandas dataframe of the csv file, make a few changes
        df = pd.read_csv(path)

        df.at[row_to_change - 1, 'num_days'] += 1
        df.at[row_to_change, 'water_dispensed'] += 500
        df.at[row_to_change + 1, 'activity_level'] = 'Moderate'

        temp_water_dispensed = df.at[row_to_change, 'water_dispensed']
        temp_water_dispensed += 1000

        df.at[row_to_change, 'water_dispensed'] = temp_water_dispensed

        df.to_csv(path, index=False)

        csv_file.close()

        edited_user_data = [
            ['734a266f', 'True', 'Chris Smith', 'Female', '42', 'Sedentary', '2000', '101', '99', '214503', '2145.03'],
            ['5d81e96d', 'True', 'Ivann Cruz', 'Male', '81', 'Active', '2200-2400', '365', '157', '727104', '1987.96'],
            ['4a273b9e', 'True', 'Ken Lee', 'Male', '4', 'Moderate', '1400-1600', '10', '3', '13045', '1304.5']
        ]

        # open file, read data from file
        with open(path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_num = 0
            for row in reader:
                if row_num == 0:
                    self.assertEqual(columns, row)
                else:
                    self.assertEqual(edited_user_data[row_num - 1], row)
                row_num += 1

        csv_file.close()

    def test_open_write_empty_read_close(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'gender', 'age', 'activity_level', 'daily_hydration',
                   'num_days', 'num_days_goal', 'water_dispensed', 'avg_intake']
        user_data = [
            ['', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '']
        ]

        # NOTE: enter the exact path for your machine to run locally
        path = ''

        # open file, write data to file
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(user_data)

        # open file, read data from file
        with open(path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_num = 0
            for row in reader:
                if row_num == 0:
                    self.assertEqual(columns, row)
                else:
                    self.assertEqual(user_data[row_num-1], row)
                row_num += 1

        csv_file.close()

    def test_file_initialization_for_boot_up(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'gender', 'age', 'activity_level', 'daily_hydration',
                   'num_days', 'num_days_goal', 'water_dispensed', 'avg_intake']
        user_data = [
            ['734a266f', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['5d81e96d', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['4d71f56d', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['fdd1a46b', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['1d4ba46b', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['dd8b9f6b', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]

        # NOTE: enter the exact path for your machine to run locally
        path = ''

        # open file, write data to file
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(user_data)

        # open file, read data from file
        with open(path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_num = 0
            for row in reader:
                if row_num == 0:
                    self.assertEqual(columns, row)
                else:
                    self.assertEqual(user_data[row_num-1], row)
                row_num += 1

        csv_file.close()


if __name__ == '__main__':
    unittest.main()
