import tkinter as tk
from tkinter import ttk
import pandas as pd
from os import path
import random
import csv
import time
from datetime import datetime

from rfid.rfid import RFID
from pump.pump import Pump


class GUI(tk.Tk):
    # file_path = "C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv"
    # file_path = "/home/kenlee/Documents/GitHub/CS179J-Smart-Water-Station-Project/data/user_data.csv"
    # file_path = "/home/pi/Desktop/CS179J-Smart-Water-Station/data/user_data.csv"
    file_path = "/home/pi/Documents/CS179J-Smart-Water-Station/data/user_data.csv"

    already_counted_goal = 0   

    def __init__(self):
        super().__init__()

        self.frame = None
        self.container = None
        self.frame_dictionary = {}
        self.frame_object_list = []

        self.csv_initialize()
        self.setup_gui()
        self.create_container()
        self.create_frames()

        self.rfid = RFID()
        self.card_uid = ''
        self.card_state = False

        self.pump = Pump()

    def setup_gui(self):
        self.title("Smart Water Station")
        self.geometry('800x480')
        self.resizable(width=False, height=False)

    def create_container(self):
        self.container = tk.Frame(self)
        self.container.pack()

    def create_frames(self):
        self.frame_object_list = [IdlePage, RFIDPage, UserRegistrationPage, UserHomeScreen, SettingsPage,
                                  DeletionConfirmationPage, DeletionPage, MoreInfoPage, ChangeAttributesPage,
                                  EditAttributes]

        for the_frame in self.frame_object_list:
            self.frame = the_frame(self, self.container)
            self.frame_dictionary[the_frame] = self.frame
            self.frame.grid(row=0, column=0, sticky="news")

        self.change_frame(IdlePage)

    def update_frame(self, f):
        self.frame = self.frame_dictionary[f]

        for the_frame in self.frame_object_list:
            self.frame.destroy()

        for the_frame in self.frame_object_list:
            self.frame = the_frame(self, self.container)
            self.frame_dictionary[the_frame] = self.frame
            self.frame.grid(row=0, column=0, sticky="news")

    def change_frame(self, f):
        self.frame = self.frame_dictionary[f]
        self.frame.tkraise()

    def csv_initialize(self):

        if not path.exists(self.file_path):
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

    def scan_rfid_card(self):
        self.rfid.scan_card()
        self.card_uid = self.rfid.get_uid()

    def check_rfid_card_registration(self):
        self.card_state = self.rfid.check_registration(self.card_uid)

    def register_card(self):
        self.rfid.register_card(self.card_uid)
        self.check_rfid_card_registration()

    def unregister_card(self):
        self.rfid.unregister_card(self.card_uid)
        self.check_rfid_card_registration()

    def get_card_uid(self):
        return self.card_uid

    def get_card_state(self):
        return self.card_state


class IdlePage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.rowconfigure(0, minsize=70, weight=1)
        self.rowconfigure(1, minsize=50, weight=1)
        self.rowconfigure(2, minsize=230, weight=1)
        self.rowconfigure(3, minsize=100, weight=1)
        self.rowconfigure(4, minsize=30, weight=1)

        self.columnconfigure(0, minsize=120, weight=1)
        self.columnconfigure(1, minsize=480, weight=0)
        self.columnconfigure(2, minsize=200, weight=1)

        self.water_data = WaterData()

        self.fact, self.source = self.water_data.get_fact_source()

        # define GUI labels and buttons
        self.idle_label = tk.Label(self, text="IDLE MODE", font=("Calibri", 12))
        self.did_you_know_label = tk.Label(self, text="Did you know?\n\n", font=("Calibri", 12, "bold"))
        self.fact_source_label = tk.Label(self, text=self.fact + "\n\n" + self.source, font=("Calibri", 12),
                                          justify="left", anchor="w")

        self.next_btn = tk.Button(self, text="-- Press this button to continue --", font=("Calibri", 12),
                                  command=lambda: container.change_frame(RFIDPage)).place(x=250, y=400)

        # structure the GUI page using a grid
        self.idle_label.grid(row=0, column=0, sticky="nw", padx=7, pady=7)
        self.did_you_know_label.grid(row=1, column=1, sticky="nw")
        self.fact_source_label.grid(row=2, column=1, sticky="nw")

        self.fact_source_label.after(15000, self.update_text)

    def update_text(self):
        self.fact, self.source = self.water_data.get_fact_source()

        self.fact_source_label.config(text=self.fact + "\n\n" + self.source, font=("Calibri", 12), justify="left",
                                      anchor="w")
        # 15000 = 15 seconds, this can change to a different value if need be
        self.fact_source_label.after(15000, self.update_text)


class RFIDPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.file_path = GUI.file_path

        self.uid = ''
        self.state = False

        self.scan_card_label = tk.Label(self, text="PLEASE SCAN YOUR RFID CARD TO CONTINUE",
                                        font=("Calibri", 20)).place(x=100,y=10)

        self.back_btn = tk.Button(self, text="Go Back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(IdlePage)).place(x=380, y=350)

        self.scan_card_btn = tk.Button(self, text="Scan your RFID Card now", font=("Calibri", 12),
                                       command=lambda: self.scan_rfid_card(container)).place(x=300, y=200)

    def scan_rfid_card(self, container):
        container.scan_rfid_card()
        container.check_rfid_card_registration()

        self.uid = container.get_card_uid()
        self.state = container.get_card_state()

        UserHomeScreen.uid = self.uid
        MoreInfoPage.uid = self.uid

        if self.state:
            # UserHomeScreen.research_data(self)
            self.update_last_login_num_days()
            container.update_frame(UserHomeScreen)
            container.change_frame(UserHomeScreen)
        else:
            container.update_frame(UserRegistrationPage)
            container.change_frame(UserRegistrationPage)

    def update_last_login_num_days(self):
        df = pd.read_csv(self.file_path)

        row_num = df.index[df['card_uid'] == self.uid].tolist()

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y %H:%M:%S")

        old_time = datetime.strptime(df.at[row_num[0], 'last_login'], "%m/%d/%Y %H:%M:%S")

        time_diff = (now - old_time).days

        if time_diff > 0:
            df.at[row_num[0], 'num_days'] += 1
            df.at[row_num[0], 'percent_dispensed_of_daily'] = 0.0
            GUI.already_counted_goal = 0

        df.at[row_num[0], 'last_login'] = date_time

        df.to_csv(self.file_path, index=False)


class UserRegistrationPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.file_path = GUI.file_path

        self.uid = ''

        valid_command_name = (self.register(self.input_validation_name), '%S')
        valid_command_age = (self.register(self.input_validation_age), '%S')

        self.welcome_new_user_screen = tk.Label(self, text="Hello, New User!", font=("Calibri", 20)).place(x=320, y=0)
        self.user_intro = tk.Label(self, text="What is your: ", font=("Calibri", 15)).place(x=240, y=120)
        self.user_name = tk.Label(self, text="Name").place(x=240, y=160)
        self.user_age = tk.Label(self, text="Age").place(x=240, y=200)
        self.input_name = tk.StringVar()
        self.usr_name_in = tk.Entry(self, width=30, textvariable=self.input_name, validate="key",
                                    validatecommand=valid_command_name).place(x=310, y=160)
        self.input_age = tk.StringVar()
        self.usr_age_in = tk.Entry(self, textvariable=self.input_age, width=30, validate="key",
                                   validatecommand=valid_command_age).place(x=310, y=200)

        self.usr_S = tk.Label(self, text="Are you: ").place(x=240, y=240)
        self.s = tk.StringVar()
        self.usr_SSelection = ttk.Combobox(self, width=7, textvariable=self.s)
        self.usr_SSelection.place(x=310, y=240)
        self.usr_SSelection['values'] = ('Male', 'Female')
        self.usr_SSelection.current()

        self.usr_S2 = tk.Label(self, text="What is your activity level? ").place(x=240, y=280)
        self.s2 = tk.StringVar()
        self.usr_SSelection2 = ttk.Combobox(self, width=20, textvariable=self.s2)
        self.usr_SSelection2.place(x=310, y=310)
        self.usr_SSelection2['values'] = ('Sedentary', 'Moderate', 'Active')
        self.usr_SSelection2.current()

        self.submit = tk.Button(self, text="Submit",
                                command=lambda: [self.save_command(container), UserHomeScreen.research_data(self), 
                                                 container.update_frame(UserHomeScreen),
                                                 container.change_frame(UserHomeScreen)]).place(x=385, y=350)

        self.go_back_btn = tk.Button(self, text="Go Back", font=("Calibri", 12),
                                     command=lambda: container.change_frame(RFIDPage)).place(x=375, y=400)

    def input_validation_name(self, keypress):
        if keypress.isalpha() or keypress.isspace():
            return True
        else:
            return False

    def input_validation_age(self, keypress):
        if keypress.isnumeric():
            return True
        else:
            return False

    def save_command(self, container):
        self.uid = container.get_card_uid()

        container.register_card()

        df = pd.read_csv(self.file_path)

        row_num = df.index[df['card_uid'] == self.uid].tolist()

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y %H:%M:%S")

        df.at[row_num[0], 'name'] = self.input_name.get()
        df.at[row_num[0], 'age'] = self.input_age.get()
        df.at[row_num[0], 'sex'] = self.s.get()
        df.at[row_num[0], 'activity_level'] = self.s2.get()
        df.at[row_num[0], 'daily_hydration_lower'] = 0.0
        df.at[row_num[0], 'daily_hydration_upper'] = 0.0
        df.at[row_num[0], 'water_dispensed'] = 0.0
        df.at[row_num[0], 'total_dispensed'] = 0.0
        df.at[row_num[0], 'percent_dispensed_of_daily'] = 0.0
        df.at[row_num[0], 'num_days'] = 1
        df.at[row_num[0], 'num_days_goal'] = 0
        df.at[row_num[0], 'avg_intake'] = 0.0
        df.at[row_num[0], 'last_login'] = date_time

        df.to_csv(self.file_path, index=False)


class UserHomeScreen(tk.Frame):
    uid = ''

    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.file_path = GUI.file_path

        self.uid = UserHomeScreen.uid

        df = pd.read_csv(self.file_path)
        row_num = df.index[df['card_uid'] == self.uid].tolist()

        if len(row_num) is 0:
            row_num.append(0)

        self.welcome_home_screen = tk.Label(self, text="Hello, " + str(df.at[row_num[0], 'name']) + "!",
                                            font=("Calibri", 20)).place(x=320, y=10)
        #self.welcome_home_screen.pack()

        self.hydration_percentage_header = tk.Label(self, text="Current Hydration Level:",
                                                    font=("Calibri", 30)).place(x=160, y=150)
        self.hydration_percentage = tk.Label(self, text=str(df.at[row_num[0], 'percent_dispensed_of_daily']) + "%",
                                             font=("Calibri", 30)).place(x=370, y=210)
        # self.dispense_label = tk.Label(self, text="Dispense Button Enabled", font=("Calibri", 12),
        #                                fg="green").place(x=340, y=320)

        self.settings_btn = tk.Button(self, text="Settings", font=("Calibri", 12),
                                      command=lambda: container.change_frame(SettingsPage)).place(x=660, y=400)
        self.logout_btn = tk.Button(self, text="Log Out", font=("Calibri", 12),
                                    command=lambda: container.change_frame(IdlePage)).place(x=380, y=400)
        self.more_info_btn = tk.Button(self, text="More Info", font=("Calibri", 12),
                                       command=lambda: [self.research_data(), container.update_frame(MoreInfoPage),
                                                        container.change_frame(MoreInfoPage)]).place(x=50, y=400)

        self.dispense_btn = tk.Button(self, text="Enable Dispenser", font=("Calibri", 12),
                                      command=lambda: [container.pump.dispense_water(container, False),
                                                       container.update_frame(UserHomeScreen),
                                                       container.change_frame(UserHomeScreen)]).place(x=340, y=320)

        df.to_csv(self.file_path, index=False)

    def research_data(self):
        """
        Make sure this is RFID Hardware Compatible
        """
        self.file_path = GUI.file_path

        self.uid = UserHomeScreen.uid

        df = pd.read_csv(self.file_path)
        row_num = df.index[df['card_uid'] == self.uid].tolist()

        if len(row_num) is 0:
            row_num.append(0)

        """
        This function needs to be called in multiple places: button to go to UserHomeScreen, 
        Registration submit button, change attributes submit button
        """

        if df.at[row_num[0], 'age'] == 2 or df.at[row_num[0], 'age'] == 3:
            df.at[row_num[0], 'daily_hydration_lower'] = 1000
            df.at[row_num[0], 'daily_hydration_upper'] = 1400

        elif df.at[row_num[0], 'sex'] == "Male":
            if 3 < df.at[row_num[0], 'age'] <= 8:
                df.at[row_num[0], 'daily_hydration_lower'] = 1400
                df.at[row_num[0], 'daily_hydration_upper'] = 1600

            elif 8 < df.at[row_num[0], 'age'] <= 13:
                df.at[row_num[0], 'daily_hydration_lower'] = 1800
                df.at[row_num[0], 'daily_hydration_upper'] = 2000

            elif 13 < df.at[row_num[0], 'age'] <= 18:
                df.at[row_num[0], 'daily_hydration_lower'] = 2400
                df.at[row_num[0], 'daily_hydration_upper'] = 2800

            elif 18 < df.at[row_num[0], 'age'] <= 30:
                df.at[row_num[0], 'daily_hydration_lower'] = 2600
                df.at[row_num[0], 'daily_hydration_upper'] = 2800

            elif 30 < df.at[row_num[0], 'age'] <= 50:
                df.at[row_num[0], 'daily_hydration_lower'] = 2400
                df.at[row_num[0], 'daily_hydration_upper'] = 2600

            elif df.at[row_num[0], 'age'] > 50:
                df.at[row_num[0], 'daily_hydration_lower'] = 2200
                df.at[row_num[0], 'daily_hydration_upper'] = 2400

        elif df.at[row_num[0], 'sex'] == "Female":
            if 3 < df.at[row_num[0], 'age'] <= 8:
                df.at[row_num[0], 'daily_hydration_lower'] = 1400
                df.at[row_num[0], 'daily_hydration_upper'] = 1600

            elif 8 < df.at[row_num[0], 'age'] <= 13:
                df.at[row_num[0], 'daily_hydration_lower'] = 1600
                df.at[row_num[0], 'daily_hydration_upper'] = 2000

            elif 13 < df.at[row_num[0], 'age'] <= 18:
                df.at[row_num[0], 'daily_hydration_lower'] = 2000
                df.at[row_num[0], 'daily_hydration_upper'] = 2000

            elif 18 < df.at[row_num[0], 'age'] <= 30:
                df.at[row_num[0], 'daily_hydration_lower'] = 2000
                df.at[row_num[0], 'daily_hydration_upper'] = 2200

            elif 30 < df.at[row_num[0], 'age'] <= 50:
                df.at[row_num[0], 'daily_hydration_lower'] = 2000
                df.at[row_num[0], 'daily_hydration_upper'] = 2000

            elif df.at[row_num[0], 'age'] > 50:
                df.at[row_num[0], 'daily_hydration_lower'] = 1800
                df.at[row_num[0], 'daily_hydration_upper'] = 1800
                
        if df.at[row_num[0], 'percent_dispensed_of_daily'] >= 100 and GUI.already_counted_goal == 0:
                df.at[row_num[0], 'num_days_goal'] += 1
                GUI.already_counted_goal = 1

        df.to_csv(self.file_path, index=False)


class SettingsPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.settings_intro_header = tk.Label(self, text="What Would You Like To Do?",
                                              font=("Calibri", 20)).place(x=210, y=0)

        self.delete_user_btn = tk.Button(self, text="Delete User", font=("Calibri", 12), bg="red",
                                         command=lambda: container.change_frame(DeletionConfirmationPage)).place(x=370,
                                                                                                                 y=100)
        self.change_user_attr_btn = tk.Button(self, text="Edit My Attributes", font=("Calibri", 12),
                                              command=lambda: container.change_frame(ChangeAttributesPage)).place(x=345,
                                                                                                                  y=200)
        self.go_back_btn = tk.Button(self, text="Go Back", font=("Calibri", 12),
                                     command=lambda: container.change_frame(UserHomeScreen)).place(x=380, y=300)


class ChangeAttributesPage(tk.Frame):
    attribute_selection = 0

    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.attr_settings_header = tk.Label(self, text="What Would You Like To Edit?",
                                             font=("Calibri", 20)).place(x=230, y=0)

        self.delete_user_btn1 = tk.Button(self, text="My Name", font=("Calibri", 12),
                                          command=lambda: [self.attribute_change(1),
                                                           container.update_frame(EditAttributes),
                                                           container.change_frame(EditAttributes)]).place(x=150, y=200)

        self.change_user_attr_btn = tk.Button(self, text="My Age", font=("Calibri", 12),
                                              command=lambda: [self.attribute_change(2),
                                                               container.update_frame(EditAttributes),
                                                               container.change_frame(EditAttributes)]).place(x=280,
                                                                                                              y=200)

        self.change_user_attr_btn = tk.Button(self, text="My Sex", font=("Calibri", 12),
                                              command=lambda: [self.attribute_change(3),
                                                               container.update_frame(EditAttributes),
                                                               container.change_frame(EditAttributes)]).place(x=390,
                                                                                                              y=200)

        self.change_user_attr_btn = tk.Button(self, text="My Activity Level", font=("Calibri", 12),
                                              command=lambda: [self.attribute_change(4),
                                                               container.update_frame(EditAttributes),
                                                               container.change_frame(EditAttributes)]).place(x=510,
                                                                                                              y=200)

        self.go_back_btn1 = tk.Button(self, text="I'm Done, Go Back", font=("Calibri", 12),
                                      command=lambda: container.change_frame(SettingsPage)).place(x=350, y=300)

    def attribute_change(self, num):
        ChangeAttributesPage.attribute_selection = num


class EditAttributes(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.file_path = GUI.file_path

        self.uid = ''

        if ChangeAttributesPage.attribute_selection == 1:
            self.userName1 = tk.Label(self, text="Name").place(x=240, y=160)
            self.inputName1 = tk.StringVar()
            self.usrNameIn1 = tk.Entry(self, width=30, textvariable=self.inputName1).place(x=310, y=160)
        elif ChangeAttributesPage.attribute_selection == 2:
            self.userAge1 = tk.Label(self, text="Age").place(x=260, y=160)
            self.inputAge1 = tk.StringVar()
            self.usrAgeIn1 = tk.Entry(self, width=30, textvariable=self.inputAge1).place(x=310, y=160)
        elif ChangeAttributesPage.attribute_selection == 3:
            self.usrS_edit = tk.Label(self, text="Are you: ").place(x=270, y=160)
            self.s_edit = tk.StringVar()
            self.usrSSelection_edit = ttk.Combobox(self, width=7, textvariable=self.s_edit)
            self.usrSSelection_edit.place(x=340, y=160)
            self.usrSSelection_edit['values'] = ('Male', 'Female')
            self.usrSSelection_edit.current()
        elif ChangeAttributesPage.attribute_selection == 4:
            self.usrS2_edit = tk.Label(self, text="What is your activity level? ").place(x=240, y=160)
            self.s2_edit = tk.StringVar()
            self.usrSSelection2_edit = ttk.Combobox(self, width=20, textvariable=self.s2_edit)
            self.usrSSelection2_edit.place(x=310, y=190)
            self.usrSSelection2_edit['values'] = ('Sedentary', 'Moderate', 'Active')
            self.usrSSelection2_edit.current()

        self.submit = tk.Button(self, text="Submit",
                                command=lambda: [self.save_command1(container), UserHomeScreen.research_data(self),
                                                 container.update_frame(UserHomeScreen),
                                                 container.change_frame(ChangeAttributesPage)]).place(x=370, y=350)

        self.back_btn = tk.Button(self, text="Go Back",
                                  command=lambda: container.change_frame(ChangeAttributesPage)).place(x=365, y=400)

    def save_command1(self, container):
        self.uid = container.get_card_uid()

        df = pd.read_csv(self.file_path)

        row_num = df.index[df['card_uid'] == self.uid].tolist()

        if ChangeAttributesPage.attribute_selection == 1:
            df.at[row_num[0], 'name'] = self.inputName1.get()

        elif ChangeAttributesPage.attribute_selection == 2:
            df.at[row_num[0], 'age'] = self.inputAge1.get()

        elif ChangeAttributesPage.attribute_selection == 3:
            df.at[row_num[0], 'sex'] = self.s_edit.get()

        elif ChangeAttributesPage.attribute_selection == 4:
            df.at[row_num[0], 'activity_level'] = self.s2_edit.get()

        df.to_csv(self.file_path, index=False)


class DeletionConfirmationPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.file_path = GUI.file_path

        self.uid = ''

        self.delete_confirm_header = tk.Label(self, text="Are You Sure?", font=("Calibri", 20)).place(x=330, y=0)
        self.delete_confirm_info_header = tk.Label(self, text="This Action Cannot Be Undone!", font=("Calibri", 20),
                                                   fg="red").place(x=210, y=120)

        self.continue_btn = tk.Button(self, text="Yes, I'm Sure", font=("Calibri", 12), bg="red",
                                      command=lambda: [self.delete_user_command(container),
                                                       container.change_frame(DeletionPage)]).place(x=500, y=280)
        self.continue_btn = tk.Button(self, text="No, Go Back", font=("Calibri", 12),
                                      command=lambda: container.change_frame(SettingsPage)).place(x=190, y=280)

    def delete_user_command(self, container):
        self.uid = container.get_card_uid()

        container.unregister_card()

        df = pd.read_csv(self.file_path)

        row_num = df.index[df['card_uid'] == self.uid].tolist()

        df.at[row_num[0], 'name'] = ' '
        df.at[row_num[0], 'age'] = 0
        df.at[row_num[0], 'sex'] = ' '
        df.at[row_num[0], 'activity_level'] = ' '
        df.at[row_num[0], 'daily_hydration_lower'] = 0.0
        df.at[row_num[0], 'daily_hydration_upper'] = 0.0
        df.at[row_num[0], 'water_dispensed'] = 0.0
        df.at[row_num[0], 'total_dispensed'] = 0.0
        df.at[row_num[0], 'percent_dispensed_of_daily'] = 0.0
        df.at[row_num[0], 'num_days'] = 0
        df.at[row_num[0], 'num_days_goal'] = 0
        df.at[row_num[0], 'avg_intake'] = 0.0
        df.at[row_num[0], 'last_login'] = ' '

        df.to_csv(self.file_path, index=False)


class DeletionPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.delete_page_header = tk.Label(self, text="User Deleted", font=("Calibri", 20)).place(x=350, y=0)
        self.delete_page_header = tk.Label(self, text="All user data and the RFID card associated\n "
                                                      "with this user has been successfully reset.",
                                           font=("Calibri", 15)).place(x=200, y=200)

        self.continue_btn = tk.Button(self, text="Continue", font=("Calibri", 12),
                                      command=lambda: container.change_frame(IdlePage)).place(x=380, y=290)


class MoreInfoPage(tk.Frame):
    uid = ''

    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.file_path = GUI.file_path

        self.uid = MoreInfoPage.uid

        df = pd.read_csv(self.file_path)
        row_num = df.index[df['card_uid'] == self.uid].tolist()

        if len(row_num) is 0:
            row_num.append(0)

        self.user_reg_stats = tk.Label(self, text="Your Attributes:", font=("Calibri", 30)).place(x=250, y=10)
        self.attr_1 = tk.Label(self, text="Age:  " + str(df.at[row_num[0], 'age']),
                               font=("Calibri", 12)).place(x=345, y=120)
        self.attr_2 = tk.Label(self, text="Sex:  " + df.at[row_num[0], 'sex'],
                               font=("Calibri", 12)).place(x=345, y=145)
        self.attr_3 = tk.Label(self, text="Activity Level:  " + df.at[row_num[0], 'activity_level'],
                               font=("Calibri", 12)).place(x=270, y=170)
        self.attr_4 = tk.Label(self,
                               text="Recommended Range For Daily Hydration:  "
                                    + str(df.at[row_num[0], 'daily_hydration_lower']) + " mL to "
                                    + str(df.at[row_num[0], 'daily_hydration_upper']) + " mL",
                               font=("Calibri", 12)).place(x=40, y=195)

        self.attr_5 = tk.Label(self,
                               text="Number of Days Where Goal Has Been Met:  "
                                    + str(df.at[row_num[0], 'num_days_goal']),
                               font=("Calibri", 12)).place(x=30, y=220)

        self.attr_6 = tk.Label(self, text="Water Dispensed Last Session:  " 
                               + str(df.at[row_num[0], 'water_dispensed'] * 1000) + " mL",
                               font=("Calibri", 12)).place(x=135, y=245)
        self.attr_7 = tk.Label(self, text="Your Average Water Intake:  " 
                               + str(df.at[row_num[0], 'avg_intake'] * 1000) + " mL",
                               font=("Calibri", 12)).place(x=155, y=270)

        self.back_btn = tk.Button(self, text="Go Back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(UserHomeScreen)).place(x=380, y=350)
                                  
        self.disclaimer = tk.Label(self, text="*The recommended ranges are based off of estimates\n and may not be representative of your actual needs",
                               font=("Calibri", 8)).place(x=35, y=400)

        df.to_csv(self.file_path, index=False)


class WaterData:
    def __init__(self):
        self.factDictionary = {"Water covers about 71% of the earth's surface.":
                                   "- United States Bureau of Reclamation",

                               "2.5% of the earth's fresh water is unavailable: locked up \n"
                               "in glaciers, polar ice caps, atmosphere, and soil; \n"
                               "highly polluted; or lies too far under the earth's surface \n"
                               "to be extracted at an affordable cost. ":
                                   "- United States Bureau of Reclamation",

                               "97% of the earth's water is found in the oceans \n"
                               "(too salty for drinking, growing crops, and most industrial \n"
                               "uses except cooling).":
                                   "- United States Bureau of Reclamation",

                               "If the world's water supply were only 100 liters (26 gallons), \n"
                               "our usable water supply of fresh water would be only about \n"
                               "0.003 liter (one-half teaspoon). ":
                                   "- United States Bureau of Reclamation",

                               "A leak that fills up a coffee cup in 10 minutes will waste over\n"
                               "3,000 gallons of water in a year. That's 65 glasses of water every\n"
                               "day for a year.":
                                   "- United States Bureau of Reclamation",

                               "There is the same amount of water on Earth as there was when \n"
                               "the Earth was formed. The water from your faucet could contain \n"
                               "molecules that dinosaurs drank.":
                                   "- U.S. Environmental Protection Agency",

                               "A person can live about a month without food, but only\n"
                               "about a week without water.":
                                   "- U.S. Environmental Protection Agency",

                               "Water regulates the Earth's temperature. It also regulates the\n"
                               "temperature of the human body, carries nutrients and oxygen to \n"
                               "cells, cushions joints, protects organs and tissues, and removes wastes.":
                                   "- U.S. Environmental Protection Agency",

                               "There aren't many qualities that are true of all life on Earth, \n"
                               "but the need for water is one of them. It's in all living things, \n"
                               "whether they live at the bottom of the ocean or the driest desert.":
                                   "- National Aeronautics and Space Administration",

                               "It's possible that comets made regular water deliveries to Earth. \n"
                               "It would take a lot of comets to fill the ocean, but comets could \n"
                               "well have made a big contribution.":
                                   "- National Aeronautics and Space Administration",

                               "A newborn baby is 78 percent water. Adults are 55-60 percent water.\n"
                               "Water is involved in just about everything our body does.":
                                   "- National Aeronautics and Space Administration",

                               "Water is called the \"universal solvent\" because it dissolves more \n"
                               "substances than any other liquid. This means that wherever water goes, \n"
                               "either through the ground or through our bodies, it takes along valuable\n"
                               "chemicals, minerals, and nutrients.":
                                   "- United States Geological Survey",

                               "Pure water has a neutral pH of 7, which is neither acidic (less than 7)\n"
                               "nor basic (greater than 7).":
                                   "- United States Geological Survey",

                               "The water molecule is highly cohesive - it is very sticky, meaning water\n"
                               "molecules stick to each other. Water is the most cohesive among the\n"
                               "non-metallic liquids.":
                                   "- United States Geological Survey",
                               }

    def get_fact_source(self):
        return random.choice(list(self.factDictionary.items()))


if __name__ == '__main__':
    root = GUI()
    root.mainloop()
