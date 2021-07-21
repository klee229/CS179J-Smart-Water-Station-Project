from Tkinter import *
import tkinter as tk
from tkinter import ttk


root = Tk()
#size of LED screen
root.geometry('800x480')
root.title('Registration')

welcome = Label(root, text = "Hello, User!", font = ("Arial", 15)).place(x=350,y=0)

userName = Label(root, text = "Name").place(x=240,y=160)
userAge = Label(root, text = "Age").place(x=240,y=200)

usrNameIn = Entry(root,width = 30).place(x=310,y=160)
usrAgeIn = Entry(root,width = 30).place(x=310,y=200)

  

usrS = Label(root, text = "Are you: ").place(x=240,y=240)
  
# Combobox creation
s = StringVar()
usrSSelection = ttk.Combobox(root, width = 15, textvariable = s)
usrSSelection.place(x=310,y=240)
  
# Adding combobox drop down list
usrSSelection['values'] = ('Male', 'Female')
  
usrSSelection.current()

submit = Button(root,text="Submit").place(x=350, y = 300)

root.mainloop()