import unittest
import csv
import pandas as pd


class TestCSVFile(unittest.TestCase):

    # NOTE: all items in user_data converted to str from int or float, this way we compare string to string for testing

    def test_open_write_read_close(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'age', 'sex', 'activity_level',
                   'daily_hydration_lower', 'daily_hydration_upper', 'water_dispensed', 'total_dispensed',
                   'percent_dispensed_of_daily', 'num_days', 'num_days_goal', 'avg_intake', 'last_login'
                   ]

        user_data = [
            ['734a266f', 'True', 'name one', '5', 'Male', 'Sedentary', '1400', '1600', '0', '100000', '0.0', '1', '0',
             '1517.0', '20/08/2021 05:42:21'],
            ['5d81e96d', 'True', 'name two', '12', 'Female', 'Sedentary', '1600', '2000', '200', '200000', '20.0', '14',
             '12', '1984.0', '11/07/2021 07:15:09'],
            ['4d71f56d', 'True', 'name three', '17', 'Male', 'Moderate', '2400', '2800', '500', '300000', '50.0', '28',
             '19', '1000.0', '20/08/2021 16:58:59'],
            ['fdd1a46b', 'True', 'name four', '29', 'Female', 'Moderate', '2000', '2200', '1300', '400000', '130.0',
             '33', '3', '0.0', '20/08/2021 24:24:24'],
            ['1d4ba46b', 'True', 'name five', '48', 'Male', 'Active', '2400', '2600', '1800', '500000', '180.0', '99',
             '99', '2256.0', '20/08/2021 17:36:10'],
            ['dd8b9f6b', 'True', 'name six', '76', 'Female', 'Active', '1800', '1800', '2400', '600000', '240.0', '257',
             '202', '1234.0', '01/01/1970 00:00:00']
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
                    self.assertEqual(user_data[row_num - 1], row)
                row_num += 1

        csv_file.close()

    def test_reopen_read_close(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'age', 'sex', 'activity_level',
                   'daily_hydration_lower', 'daily_hydration_upper', 'water_dispensed', 'total_dispensed',
                   'percent_dispensed_of_daily', 'num_days', 'num_days_goal', 'avg_intake', 'last_login'
                   ]

        user_data = [
            ['734a266f', 'True', 'name one', '5', 'Male', 'Sedentary', '1400', '1600', '0', '100000', '0.0', '1', '0',
             '1517.0', '20/08/2021 05:42:21'],
            ['5d81e96d', 'True', 'name two', '12', 'Female', 'Sedentary', '1600', '2000', '200', '200000', '20.0', '14',
             '12', '1984.0', '11/07/2021 07:15:09'],
            ['4d71f56d', 'True', 'name three', '17', 'Male', 'Moderate', '2400', '2800', '500', '300000', '50.0', '28',
             '19', '1000.0', '20/08/2021 16:58:59'],
            ['fdd1a46b', 'True', 'name four', '29', 'Female', 'Moderate', '2000', '2200', '1300', '400000', '130.0',
             '33', '3', '0.0', '20/08/2021 24:24:24'],
            ['1d4ba46b', 'True', 'name five', '48', 'Male', 'Active', '2400', '2600', '1800', '500000', '180.0', '99',
             '99', '2256.0', '20/08/2021 17:36:10'],
            ['dd8b9f6b', 'True', 'name six', '76', 'Female', 'Active', '1800', '1800', '2400', '600000', '240.0', '257',
             '202', '1234.0', '01/01/1970 00:00:00']
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
        example_user = ['1a2b3c4d', 'True', 'Test User', '76', 'Female', 'Active', '2000', '2000', '4000', '900000',
                        '4457.0', '400', '235', '1578.0', '02/12/1970 01:02:03']

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
        columns = ['card_uid', 'registration_state', 'name', 'age', 'sex', 'activity_level',
                   'daily_hydration_lower', 'daily_hydration_upper', 'water_dispensed', 'total_dispensed',
                   'percent_dispensed_of_daily', 'num_days', 'num_days_goal', 'avg_intake', 'last_login'
                   ]

        user_data = [
            ['734a266f', 'True', 'name one', '5', 'Male', 'Sedentary', '1400', '1600', '0', '100000', '0.0', '1', '0',
             '1517.0', '20/08/2021 05:42:21'],
            ['5d81e96d', 'True', 'name two', '12', 'Female', 'Sedentary', '1600', '2000', '200', '200000', '20.0', '14',
             '12', '1984.0', '11/07/2021 07:15:09'],
            ['4d71f56d', 'True', 'name three', '17', 'Male', 'Moderate', '2400', '2800', '500', '300000', '50.0', '28',
             '19', '1000.0', '20/08/2021 16:58:59'],
            ['fdd1a46b', 'True', 'name four', '29', 'Female', 'Moderate', '2000', '2200', '1300', '400000', '130.0',
             '33', '3', '0.0', '20/08/2021 24:24:24'],
            ['1d4ba46b', 'True', 'name five', '48', 'Male', 'Active', '2400', '2600', '1800', '500000', '180.0', '99',
             '99', '2256.0', '20/08/2021 17:36:10'],
            ['dd8b9f6b', 'True', 'name six', '76', 'Female', 'Active', '1800', '1800', '2400', '600000', '240.0', '257',
             '202', '1234.0', '01/01/1970 00:00:00']
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
            ['734a266f', 'True', 'name one', '5', 'Male', 'Sedentary', '1400', '1600', '0', '100000', '0.0', '2', '0',
             '1517.0', '20/08/2021 05:42:21'],
            ['5d81e96d', 'True', 'name two', '12', 'Female', 'Sedentary', '1600', '2000', '1700', '200000', '20.0',
             '14',
             '12', '1984.0', '11/07/2021 07:15:09'],
            ['4d71f56d', 'True', 'name three', '17', 'Male', 'Moderate', '2400', '2800', '500', '300000', '50.0', '28',
             '19', '1000.0', '20/08/2021 16:58:59'],
            ['fdd1a46b', 'True', 'name four', '29', 'Female', 'Moderate', '2000', '2200', '1300', '400000', '130.0',
             '33', '3', '0.0', '20/08/2021 24:24:24'],
            ['1d4ba46b', 'True', 'name five', '48', 'Male', 'Active', '2400', '2600', '1800', '500000', '180.0', '99',
             '99', '2256.0', '20/08/2021 17:36:10'],
            ['dd8b9f6b', 'True', 'name six', '76', 'Female', 'Active', '1800', '1800', '2400', '600000', '240.0', '257',
             '202', '1234.0', '01/01/1970 00:00:00']
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
        columns = ['card_uid', 'registration_state', 'name', 'age', 'sex', 'activity_level',
                   'daily_hydration_lower', 'daily_hydration_upper', 'water_dispensed', 'total_dispensed',
                   'percent_dispensed_of_daily', 'num_days', 'num_days_goal', 'avg_intake', 'last_login'
                   ]

        user_data = [
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
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
                    self.assertEqual(user_data[row_num - 1], row)
                row_num += 1

        csv_file.close()

    def test_file_initialization_for_boot_up(self):
        # example users for testing
        columns = ['card_uid', 'registration_state', 'name', 'age', 'sex', 'activity_level',
                   'daily_hydration_lower', 'daily_hydration_upper', 'water_dispensed', 'total_dispensed',
                   'percent_dispensed_of_daily', 'num_days', 'num_days_goal', 'avg_intake', 'last_login'
                   ]

        user_data = [
            ['734a266f', 'False', ' ', '0', ' ', ' ', '0', '0', '0', '0', '0.0', '0', '0', '0.0', ' '],
            ['5d81e96d', 'False', ' ', '0', ' ', ' ', '0', '0', '0', '0', '0.0', '0', '0', '0.0', ' '],
            ['4d71f56d', 'False', ' ', '0', ' ', ' ', '0', '0', '0', '0', '0.0', '0', '0', '0.0', ' '],
            ['fdd1a46b', 'False', ' ', '0', ' ', ' ', '0', '0', '0', '0', '0.0', '0', '0', '0.0', ' '],
            ['1d4ba46b', 'False', ' ', '0', ' ', ' ', '0', '0', '0', '0', '0.0', '0', '0', '0.0', ' '],
            ['dd8b9f6b', 'False', ' ', '0', ' ', ' ', '0', '0', '0', '0', '0.0', '0', '0', '0.0', ' ']
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
                    self.assertEqual(user_data[row_num - 1], row)
                row_num += 1

        csv_file.close()


if __name__ == '__main__':
    unittest.main()
