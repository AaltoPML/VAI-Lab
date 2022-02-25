# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:21:01 2022

@author: sevillc1
"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfile
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd
import Inputs

dirpath = os.getcwd()

bg_colour ='#19232d'

# Define the root TKinter window
root = Tk()
root.title('User feedback adaptation')
root.iconbitmap(dirpath+'\\Icons\\UFAIcon.ico')
root['bg'] = bg_colour

my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(dirpath, 'Icons\\UFAIcon_name.png')).resize((600, 400)))
my_label = Label(image = my_img1, bg = bg_colour)
my_label.grid(column = 0, row = 0, rowspan = 10, columnspan = 4)

def input_data(cl, root, destroy = True):
    if destroy:
        for widgets in root.winfo_children():
            widgets.destroy()
    cl(root)
     
my_label = Label(text = 'Choose your prefered method to give feedback to the model.' , pady= 10, font=("Arial", 12), bg = bg_colour, fg = 'white')
my_label.grid(column = 0, row = 11,columnspan = 4)

button_speak = Button(root, text = 'Speak', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.speak_mlbl, root)).grid(column = 0,row = 19)
button_write = Button(root, text = 'Write', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.writen_mlbl, root)).grid(column = 1,row = 19)
button_manual = Button(root, text = 'Manual input', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.manual_mlbl, root)).grid(column = 2,row = 19)
button_upload = Button(root, text = 'Upoad file', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.upload_mlbl, root, False)).grid(column = 3,row = 19)

root.mainloop()

# print(binary_data)