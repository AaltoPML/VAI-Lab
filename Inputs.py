# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 11:47:53 2022

@author: Sevisal
"""

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, askopenfilename
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd

class manual_mlbl:
    
    global save_path
    global saved
    save_path = ''
    saved = True
    
    def expand2square(self, pil_img, background_color):
        " Adds padding to make the image a square."
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result

    def check_quit(self):
        global saved
        if not saved:
            response = messagebox.askokcancel("Are you sure you want to leave?", "Do you want to leave the program without saving?")
            if response:
                self.master.destroy()
        else:
            self.master.destroy()
    
    def open_file(self):
        global save_path
        save_path = filedialog.askopenfile(mode='r+')
        if save_path is not None:
            t = save_path.read()
            # textentry.delete('0.0', 'end')
            # textentry.insert('0.0', t)
            # textentry.focus()
            
    def save_file_as(self):
        global save_path
        save_path = asksaveasfile(mode='w')
        save_file()
        
    def save_file(self):
        global save_path
        global saved
        if save_path == '':
            save_path = asksaveasfile(defaultextension = '.txt', filetypes = [('Text file', '.txt'), ('CSS file', '.css'), ('All Files', '*.*')])
        if save_path is not None: # asksaveasfile return `None` if dialog closed with "cancel".
            filedata = pd.DataFrame(self.binary_data, columns = self.class_list).to_string()
            save_path.write(filedata)
            saved = True
            
    def forward_back(self, image_number):
        " Forward button to continue to the next image in the folder."
        
        # Print the corresponding image
        self.my_label.grid_forget()
        self.my_label = Label(image=self.image_list[image_number-1])
        
        # Update button commands
        self.button_forw = Button(self.master, image = self.forw_img, bg = self.master['bg'], command = lambda: self.forward_back(image_number+1)).grid(column = 2,row = 19)
        self.button_back = Button(self.master, image = self.back_img, bg = self.master['bg'], command = lambda: self.forward_back(image_number-1)).grid(column = 0,row = 19)
        if image_number == self.N:
            self.button_forw = Button(self.master, image = self.forw_img, bg = self.master['bg'], state = DISABLED).grid(column = 2,row = 19)
        if image_number == 1:
            self.button_back = Button(self.master, image = self.back_img, bg = self.master['bg'], state = DISABLED).grid(column = 0,row = 19)
            
        self.my_label.grid(column=0, row=0, rowspan = 10, columnspan=3)
        
        # Classes buttons
        var = {}
        for i,cl in enumerate(self.class_list):
            # print(binary_data[image_number-1,i])
            var[i] = IntVar(value=self.binary_data[image_number-1,i])
            # I can not make this be selected when going backwards or forward if it was previously selected.
            self.button_cl[cl] = Checkbutton(self.master, text = cl, fg = 'white', bg = self.master['bg'], selectcolor = 'black', height = 3, width = 20, variable = var[i], command=(lambda i=i: self.onPress(image_number-1,i)))
            self.button_cl[cl].grid(column = 4,row = i)
            
        # Status bar    
        status = Label(self.master, text='Image ' + str(image_number) + ' of '+str(self.N), bd = 1, relief = SUNKEN, anchor = E, fg = 'white', bg = self.master['bg'])
        status.grid(row=20, column=0, columnspan=4, pady = 10, sticky = W+E)
    
    # Classes buttons
    def onPress(self, n,i):
        global saved              
        self.binary_data[n,i] = not self.binary_data[n,i]
        saved = False
        
    def __init__(self, master):

        dirpath = os.getcwd()
        self.master = master
        
        self.class_list = ['Atelectasis', 'Cardiomelagy', 'Effusion', 'Infiltration', 
                      'Mass', 'Nodule', 'Pneumonia', 'Pneumothorax']
        
        pixels = 500
        path = os.path.join(dirpath, 'Example_images')
        self.N = len(os.listdir(path))
        
        # Create a list with all the available (I have tried reading the file when placing it but wasn't able to)
        self.image_list = []
        for f in os.listdir(path):
            self.image_list.append(ImageTk.PhotoImage(self.expand2square(Image.open(os.path.join(path, f)), (0, 0, 0)).resize((pixels, pixels)))) # (0, 0, 0) is the padding colour
        
        # Status bar in the lower part of the window
        status = Label(self.master, text='Image 1 of '+str(self.N), bd = 1, relief = SUNKEN, anchor = E, fg = 'white', bg = self.master['bg'])
        status.grid(row=20, column=0, columnspan=4, pady = 10, sticky = W+E)
        
        # Inital window
        
        self.my_label = Label(image = self.image_list[0], bg = self.master['bg'])
        self.my_label.grid(column = 0, row = 0, rowspan = 10, columnspan = 3)   
    
        # Buttons initialisation
        self.back_img = ImageTk.PhotoImage(Image.open(dirpath+'\\Icons\\back_arrow.png').resize((150, 50)))
        self.forw_img = ImageTk.PhotoImage(Image.open(dirpath+'\\Icons\\forw_arrow.png').resize((150, 50)))
        self.button_back = Button(self.master, image = self.back_img, bg = self.master['bg'], state = DISABLED).grid(column = 0,row = 19)
        self.button_save = Button(self.master, text = 'Save', fg = 'white', bg = master['bg'], height = 3, width = 20, command = self.save_file).grid(column = 1,row = 19)
        self.button_forw = Button(self.master, image = self.forw_img, bg = self.master['bg'], command = lambda: self.forward_back(2)).grid(column = 2,row = 19)
        self.button_quit = Button(self.master, text = 'Exit', fg = 'white', bg = self.master['bg'], height = 3, width = 20, command = self.check_quit).grid(column = 4,row = 19)
            
        
        self.binary_data = np.zeros((self.N, len(self.class_list)))
        self.button_cl = {}
        var = {}
        for i,cl in enumerate(self.class_list):
            var[i] = IntVar(value=self.binary_data[0,i])
            self.button_cl[cl] = Checkbutton(self.master, text = cl, fg = 'white', bg = self.master['bg'], selectcolor = 'black', height = 3, width = 20, variable = var[i], onvalue=1, offvalue=0, command=(lambda i=i: self.onPress(0,i)))
            self.button_cl[cl].grid(column = 4,row = i)

class writen_mlbl:
    def __init__(self, master):
        messagebox.showwarning("Error", "This functionality is not yet implemented.")
        
class speak_mlbl:
    def __init__(self, master):
        messagebox.showwarning("Error", "This functionality is not yet implemented.")     
        
class upload_mlbl:
    def __init__(self, master):
        master.filename = askopenfilename(initialdir = os.getcwd(), title = 'Select a file', defaultextension = '.txt', filetypes = [('Text file', '.txt'), ('CSS file', '.css'), ('All Files', '*.*')])
        if master.filename is not None:
            messagebox.showinfo("Success", "Feedback correctly uploaded.")