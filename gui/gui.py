import tkinter as tk
import random


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
        self.frame_object_list = [IdlePage, RFIDPage]

        for the_frame in self.frame_object_list:
            self.frame = the_frame(self, self.container)
            self.frame_dictionary[the_frame] = self.frame
            self.frame.grid(row=0, column=0, sticky="news")

        self.change_frame(IdlePage)

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
        self.next_btn = tk.Button(self, text="-- Press any button to continue --", font=("Calibri", 12),
                                  command=lambda: container.change_frame(RFIDPage))

        # structure the GUI page using a grid
        self.idle_label.grid(row=0, column=0, sticky="nw", padx=7, pady=7)
        self.water_cap_label.grid(row=0, column=2, sticky="ne", padx=7, pady=7)
        self.did_you_know_label.grid(row=1, column=1, sticky="nw")
        self.fact_source_label.grid(row=2, column=1, sticky="nw")
        self.next_btn.grid(row=3, column=0, columnspan=3, sticky="s")


class RFIDPage(tk.Frame):
    def __init__(self, container, parent):
        tk.Frame.__init__(self, parent)

        self.scan_card_label = tk.Label(self, text="PLEASE SCAN YOUR RFID CARD TO CONTINUE", font=("Calibri", 12))
        self.scan_card_label.grid(row=0, column=0)

        self.back_btn = tk.Button(self, text="go back", font=("Calibri", 12),
                                  command=lambda: container.change_frame(IdlePage))
        self.back_btn.grid(row=0, column=1)


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
                                   "- United States Bureau of Reclamation"}

    def get_water_cap(self):
        return self.water_cap

    def get_fact_source(self):
        return random.choice(list(self.factDictionary.items()))


if __name__ == '__main__':
    root = GUI()
    root.mainloop()
