import tkinter as tk
import random
import csv
import os
import time
import pandas as pd
from os import path
from tkinter import ttk
from tkinter.ttk import Button
from tkinter import *

from pandas.core.frame import DataFrame




class GUI(tk.Tk):
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

    def setup_gui(self):
        self.title("Smart Water Station")
        self.geometry('800x480')
        self.resizable(width=False, height=False)

    def create_container(self):
        self.container = tk.Frame(self)
        self.container.pack()

    def create_frames(self):
        self.frame_object_list = [IdlePage, RFIDPage, UserRegistrationPage, UserHomeScreen, SettingsPage, DeletionConfirmationPage ,DeletionPage, MoreInfoPage]

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
        file_path = "C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv"

        if not path.exists(file_path):
            columns = ['card_uid', 'registration_state', 'name', 'sex', 'age', 'activity_level', 'daily_hydration',
            'num_days', 'num_days_goal', 'water_dispensed', 'avg_intake']

            user_data = [
                ['734a266f', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['5d81e96d', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['4d71f56d', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['fdd1a46b', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['1d4ba46b', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['dd8b9f6b', 'False', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            ]
    
            # open file, write data to file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(columns)
                writer.writerows(user_data)

            csv_file.close()
    
        else:
        # create pandas dataframe of the csv file
    
            df = pd.read_csv(file_path)


            df.to_csv(file_path, index=False)
    
    
    


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
        self.water_cap = self.water_data.get_water_cap()
        self.fact, self.source = self.water_data.get_fact_source()

        # define GUI labels and buttons
        self.idle_label = tk.Label(self, text="IDLE MODE", font=("Calibri", 12))
        self.water_cap_label = tk.Label(self, text=str(self.water_cap) + " % H2O Capacity", font=("Calibri", 12)).place(x=650,y=5)
        self.did_you_know_label = tk.Label(self, text="Did you know?\n\n", font=("Calibri", 12, "bold"))
        self.fact_source_label = tk.Label(self, text=self.fact + "\n\n" + self.source, font=("Calibri", 12),
                                          justify="left", anchor="w")
        
        self.fact_source_label.after(15000, self.update_text)   
        
        self.next_btn = tk.Button(self, text="-- Press this button to continue --", font=("Calibri", 12),
                                  command=lambda: container.change_frame(RFIDPage))

        # structure the GUI page using a grid
        self.idle_label.grid(row=0, column=0, sticky="nw", padx=7, pady=7)
       # self.water_cap_label.grid(row=0, column=2, sticky="ne", padx=7, pady=7)
        self.did_you_know_label.grid(row=1, column=1, sticky="nw")
        self.fact_source_label.grid(row=2, column=1, sticky="nw")
        self.next_btn.grid(row=3, column=0, columnspan=3, sticky="s")

        
            

    def update_text(self):
        self.fact, self.source = self.water_data.get_fact_source()
        self.fact_source_label.config(text = self.fact + "\n\n" + self.source, font=("Calibri", 12),
                                          justify="left", anchor="w")
        #15000 = 15 seconds, this can change to a different value if need be
        self.fact_source_label.after(15000, self.update_text)

class UserRegistrationPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)
        
            

        self.welcome_new_user_screen = tk.Label(self, text = "Hello, New User!", font = ("Calibri", 12)).place(x=350,y=0)
        
        self.userIntro = tk.Label(self, text = "What is your: ", font = ("Calibri", 15)).place(x=240,y=120)
        self.userName = tk.Label(self, text = "Name").place(x=240,y=160)
        self.userAge = tk.Label(self, text = "Age").place(x=240,y=200)

        self.inputName = tk.StringVar()
        self.usrNameIn = tk.Entry(self, width = 30, textvariable = self.inputName).place(x=310,y=160)

        self.inputAge = tk.StringVar()
        self.usrAgeIn = tk.Entry(self, textvariable = self.inputAge, width = 30).place(x=310,y=200)
        
        self.usrS = tk.Label(self, text = "Are you: ").place(x=240,y=240)
        self.s = tk.StringVar()
        self.usrSSelection = ttk.Combobox(self, width = 7, textvariable = self.s)
        self.usrSSelection.place(x=310,y=240)
        self.usrSSelection['values'] = ('Male', 'Female')
        self.usrSSelection.current()

        self.usrS2 = tk.Label(self, text = "What is your activity level? ").place(x=240,y=280)
        self.s2 = tk.StringVar()
        self.usrSSelection2 = ttk.Combobox(self, width = 20, textvariable = self.s2)
        self.usrSSelection2.place(x=310,y=310)
        self.usrSSelection2['values'] = ('No Activity', 'Low Activity', 'Moderate Activity', 'High Activity', 'Extreme Activity')
        self.usrSSelection2.current()
      
        self.submit = tk.Button(self,text="Submit", command=lambda: [self.save_command(), container.update_frame(UserHomeScreen), container.change_frame(UserHomeScreen)]).place(x=350, y = 350)
        


    def save_command(self):
            
          
            df = pd.read_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv")   

            
            df.at[0, 'name'] = self.inputName.get()
            df.at[0, 'age'] = self.inputAge.get()
            df.at[0, 'sex'] = self.s.get()
            df.at[0, 'activity_level'] = self.s2.get()
            df.at[0, 'registration_state'] = True


            df.to_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv", index=False)
         
       
            
            
            

           
class UserHomeScreen(tk.Frame):
    def __init__(self, container, parent):
      
        tk.Frame.__init__(self, parent)
             
        #Todo: Make this compatible with multiple users use pandas and use if/else statments with increments of row number
       

        #for final project need to change path to actual Raspberry Pi
        df = pd.read_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv")   
        df.to_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv", index=False)

        
        
       
        self.welcome_home_screen = tk.Label(self, text = "Hello, " + str(df.at[0, 'name']) + "!", font = ("Calibri", 20)).place(x=350,y=5)

        self.hydrationpercentage_header = tk.Label(self, text="Current Hydration Level:", font = ("Calibri", 30)).place(x=220,y=150)

        self.hydrationpercentage = tk.Label(self, text="30 %", font = ("Calibri", 30)).place(x=380,y=210)

        self.settings_btn = tk.Button(self, text="Settings", font=("Calibri", 12),
                                  command=lambda: container.change_frame(SettingsPage)).place(x=700,y=420)

        self.logout_btn = tk.Button(self, text="Log Out", font=("Calibri", 12),
                                  command=lambda: container.change_frame(IdlePage)).place(x=400,y=420)

        self.Dispense_label = tk.Label(self, text= "Dispense Button Enabled", font = ("Calibri", 12), fg="green").place(x=340,y=320)

        self.moreinfo_btn = tk.Button(self, text="More Info", font=("Calibri", 12),
                                  command=lambda: container.change_frame(MoreInfoPage)).place(x=50,y=420)

       


class SettingsPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.settings_intro_header = tk.Label(self, text = "What Would You Like To Do?", font = ("Calibri", 20)).place(x=250,y=0)

        self.delete_user_btn = tk.Button(self, text="Delete User", font=("Calibri", 12), bg="red",
                                  command=lambda: container.change_frame(DeletionConfirmationPage)).place(x=370,y=100)
        
        self.go_back_btn = tk.Button(self, text="Go Back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(UserHomeScreen)).place(x=380,y=200)


class DeletionConfirmationPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.deleteconfirm_header = tk.Label(self, text = "Are You Sure?", font = ("Calibri", 20)).place(x=350,y=0)

        self.delete_confirminfo_header = tk.Label(self, text = "This Action Cannot Be Undone!", font = ("Calibri", 20),fg="red").place(x=250,y=100)

        self.continue_btn = tk.Button(self, text="Yes, I'm Sure", font=("Calibri", 12), bg="red",
                                  command=lambda: [self.deleteuser_command(), container.change_frame(DeletionPage)]).place(x=500,y=280)

        self.continue_btn = tk.Button(self, text="No, Go Back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(SettingsPage)).place(x=250,y=280)

    def deleteuser_command(self):
        
        #for final project need to change path to actual Raspberry Pi
        df = pd.read_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv")  
        
        df.at[0, 'name'] = ' '
        df.at[0, 'age'] = ' '
        df.at[0, 'sex'] = ' '
        df.at[0, 'activity_level'] = ' '
        df.at[0, 'registration_state'] = False

        #for final project need to change path to actual Raspberry Pi
        df.to_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv", index=False)
        

class DeletionPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)


    

        self.delete_page_header = tk.Label(self, text = "User Deleted", font = ("Calibri", 20)).place(x=350,y=0)

        self.delete_page_header = tk.Label(self, text = "All user data and the RFID card associated\n with this user has been successfully reset.", font = ("Calibri", 12)).place(x=280,y=230)

        self.continue_btn = tk.Button(self, text="Continue", font=("Calibri", 12),
                                  command=lambda: container.change_frame(IdlePage)).place(x=380,y=280)


class MoreInfoPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self,parent)

        df = pd.read_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv")   
        df.to_csv("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv", index=False)

        self.user_reg_stats = tk.Label(self, text= "Your Attributes:", font = ("Calibri", 30)).place(x=250,y=10)

        self.attr_1 = tk.Label(self, text= "Age: " + str(df.at[0, 'age']), font = ("Calibri", 12)).place(x=250,y=120)

        self.attr_2 = tk.Label(self, text= "Sex: " + str(df.at[0, 'sex']), font = ("Calibri", 12)).place(x=250,y=145)

        self.attr_3 = tk.Label(self, text= "Activity Level: " + str(df.at[0, 'activity_level']), font = ("Calibri", 12)).place(x=250,y=170)

        self.go_back_btn = tk.Button(self, text="Go Back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(UserHomeScreen)).place(x=380,y=230)




class RFIDPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)
       

        self.scan_card_label = tk.Label(self, text="PLEASE SCAN YOUR RFID CARD TO CONTINUE", font=("Calibri", 30)).pack()
        #self.scan_card_label.grid(row=0, column=0)

        self.back_btn = tk.Button(self, text="Go Back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(IdlePage)).place(x=380,y=290)
        
        ##Mock Test For When RFID is seeing an unregistered card
        self.new_user_btn = tk.Button(self, text="New User", font=("Calibri", 12),bg="green",
                                  command=lambda: container.change_frame(UserRegistrationPage)).place(x=375,y=250)
        
        #Todo: RFID integration, if card is registered, move to homepage, if not, move to user registration page
        #need global variable: scanned RFID number, to differentiate different users


class WaterData:
    def __init__(self):
        self.water_cap = 99  # TODO: determine water_cap from the pump system

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

    def get_water_cap(self):
        return self.water_cap

    def get_fact_source(self):
        return random.choice(list(self.factDictionary.items()))


      


if __name__ == "__main__":
    root = GUI()
    root.mainloop()
