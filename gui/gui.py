import tkinter as tk
import random
import csv
import os
import time
from tkinter import ttk
from tkinter.ttk import Button
from tkinter import *


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.frame = None
        self.container = None
        self.frame_dictionary = {}
        self.frame_object_list = []

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
        self.frame_object_list = [IdlePage, RFIDPage, UserRegistrationPage, UserHomeScreen]

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
        self.water_cap_label = tk.Label(self, text=str(self.water_cap) + " % H2O Capacity", font=("Calibri", 12))
        self.did_you_know_label = tk.Label(self, text="Did you know?\n\n", font=("Calibri", 12, "bold"))
        self.fact_source_label = tk.Label(self, text=self.fact + "\n\n" + self.source, font=("Calibri", 12),
                                          justify="left", anchor="w")
        
        self.fact_source_label.after(15000, self.update_text)   
        
        self.next_btn = tk.Button(self, text="-- Press any button to continue --", font=("Calibri", 12),
                                  command=lambda: container.change_frame(RFIDPage))

        # structure the GUI page using a grid
        self.idle_label.grid(row=0, column=0, sticky="nw", padx=7, pady=7)
        self.water_cap_label.grid(row=0, column=2, sticky="ne", padx=7, pady=7)
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
            
            name = self.inputName.get()
            age = self.inputAge.get()
            sex = self.s.get()
            activitylevel = self.s2.get()
            
            
            header = ['name', 'age', 'sex', 'activitylevel']
            nameheader = [name]
            data = [[name, age, sex, activitylevel]]
            
            #for final project need to change path to actual Raspberry Pi
            f = open("C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv", 'w')
                
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(nameheader)
            writer.writerows(data)

            
            f.flush()
            f.close()
            
            
            

           
class UserHomeScreen(tk.Frame):
    def __init__(self, container, parent):
      
        tk.Frame.__init__(self, parent)

        #for final project need to change path to actual Raspberry Pi
        filepath = "C:/Users/kenle/Documents/GitHub/CS179JSmartWaterDispenserProject/data/user_data.csv"
        

        if os.stat(filepath).st_size == 0:
            thename = "Error"
        else:
            file = open(filepath)
            reader = csv.reader(file)
            data = list(reader)
            thename = str(*data[2])

        
        
        self.welcome_home_screen = tk.Label(self, text = "Hello, " + thename + "!", font = ("Calibri", 12)).place(x=350,y=0)

    


class RFIDPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)
       

        self.scan_card_label = tk.Label(self, text="PLEASE SCAN YOUR RFID CARD TO CONTINUE", font=("Calibri", 12))
        self.scan_card_label.grid(row=0, column=0)

        self.back_btn = tk.Button(self, text="go back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(IdlePage))
        
        ##Mock Test For When RFID is seeing an unregistered card
        self.new_user_btn = tk.Button(self, text="New User", font=("Calibri", 12),
                                  command=lambda: container.change_frame(UserRegistrationPage))
        self.back_btn.grid(row=0, column=1)
        self.new_user_btn.grid(row=0, column=2)


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
