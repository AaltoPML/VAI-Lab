# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:21:01 2022

@author: sevillc1
"""

from tkinter import *
from tkinter import messagebox, ttk, font
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

title_font = font.Font(family='Arial', size=12)#, weight="bold", slant="italic")

my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(dirpath, 'Icons\\UFAIcon_name.png')).resize((600, 400)))
my_label = Label(frame1, image = my_img1, bg = bg_colour)
my_label.grid(column = 0, row = 0, rowspan = 10, columnspan = 4)

def input_data(cl, root, destroy = True):
    # Sub window
    cl(root)
     
my_label = Label(frame1, text = 'Choose your prefered method to give feedback to the model.' , pady= 10, font=("Arial", 12), bg = bg_colour, fg = 'white')
my_label.grid(column = 0, row = 11,columnspan = 4)

button_speak = Button(frame1, text = 'Speak', fg = 'white', font = title_font, bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.speak_mlbl, frame1, False)).grid(column = 0,row = 19)
button_write = Button(frame1, text = 'Write', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.writen_mlbl, frame1, False)).grid(column = 1,row = 19)
button_manual = Button(frame1, text = 'Manual input', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.manual_mlbl, frame1)).grid(column = 2,row = 19)
button_canvas = Button(frame1, text = 'Interact with canvas', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.canvas_sa, frame1)).grid(column = 3,row = 19)
button_upload = Button(frame1, text = 'Upoad file', fg = 'white', font=("Arial", 12), bg = bg_colour, height = 3, width = 20, command = lambda:  input_data(Inputs.upload_mlbl, frame1, False)).grid(column = 0,row = 20)
frame1.tkraise()
root.mainloop()

# print(binary_data)