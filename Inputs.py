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
            save_path.seek(0) # Move to the first row to overwrite it
            save_path.write(filedata)
            save_path.flush() # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(save_path.fileno())
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
            
class canvas_sa:

    global save_path
    global saved
    global selected
    save_path = ''
    saved = True
        
    def draw_dot(self, event):    
        
        if self.draw.get() == 'drag':
            selected = self.canvas.find_overlapping(event.x-10, event.y-10, event.x+10, event.y+10)
            if selected:
                self.canvas.selected = selected[-1]  # select the top-most item
                self.canvas.startxy = (event.x, event.y)
            else:
                self.canvas.selected = None

        if self.draw.get()  == 'draw':
            # Draw an oval in the given co-ordinates
            self.canvas.create_oval(event.x, event.y, event.x, event.y, fill="black", width=5)
            global saved
            saved = False
            self.out_data['x'].append(event.x)
            self.out_data['y'].append(event.y)

    def on_drag(self, event):
        if self.draw.get()  == 'drag' and self.canvas.selected:
            # calculate distance moved from last position
            dx, dy = event.x-self.canvas.startxy[0], event.y-self.canvas.startxy[1]
            # move the selected item
            self.canvas.move(self.canvas.selected, dx, dy)
            # update last position
            self.canvas.startxy = (event.x, event.y)
            
    def checkered(self, line_distance):        
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, self.width, line_distance):
            self.canvas.create_line(x, 0, x, self.height, fill="#476042")
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance, self.height, line_distance):
            self.canvas.create_line(0, y, self.width, y, fill="#476042")   
            
    def check_quit(self, master):
        global saved
        if not saved:
            response = messagebox.askokcancel("Are you sure you want to leave?", "Do you want to leave the program without saving?")
            if response:
                master.destroy()
        else:
            master.destroy()
            
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
            filedata = pd.DataFrame(self.out_data, columns = ['x', 'y']).to_string()
            save_path.seek(0) # Move to the first row to overwrite it
            save_path.write(filedata)
            save_path.flush() # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(save_path.fileno())
            saved = True
    
    def upload_sa(self):
        filename = askopenfilename(initialdir = os.getcwd(), title = 'Select a file', defaultextension = '.txt', filetypes = [('Text file', '.txt'), ('CSS file', '.css'), ('All Files', '*.*')])
        if filename is not None:
            data = open(filename,'r')
            read = False
            for point in data:
                if read:
                    i, x, y = point.split()
                    # Draw an oval in the given co-ordinates
                    self.canvas.create_oval(x, y, x, y,fill="grey", width=5)
                    self.out_data['x'].append(x)
                    self.out_data['y'].append(y)
                else:
                    read = True
    def reset(self):
        msg = messagebox.askyesnocancel('Info', 'Are you sure you want to reset the canvas?')
        if msg:
            self.canvas.delete(ALL)
            self.checkered(10)
            self.out_data = {'x': [], 'y': []} #coordinates
            
    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerM(self,event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        
    def __init__(self, master):
        self.out_data = {'x': [], 'y': []} #coordinates
        
        # Create a canvas widget
        self.width, self.height = 600, 600
        self.canvas=Canvas(master, width=self.width, height=self.height, background="white")
        self.canvas.grid(row=0, column=0, columnspan=4)
        self.checkered(10)
        self.canvas.bind('<Button-1>', self.draw_dot)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)
        
        self.draw = StringVar()
        self.draw.set('draw')
        # Buttons and text under the canvas
        # message = Label( master, text = "Click to draw", fg = 'white' , bg = master['bg']).grid(row=19, column=1, columnspan = 2)
        # variable = IntVar() 
        self.button_draw = Radiobutton(master, text = 'Draw', fg = 'white', bg = master['bg'], height = 3, width = 20, var = self.draw, selectcolor = 'black', value = 'draw').grid(column = 0,row = 18, columnspan = 2)
        self.button_drag = Radiobutton(master, text = 'Move', fg = 'white', bg = master['bg'], height = 3, width = 20, var = self.draw, value = 'drag', selectcolor = 'black').grid(column = 2,row = 18, columnspan = 2)
        self.button_save = Button(master, text = 'Save', fg = 'white', bg = master['bg'], height = 3, width = 20, command = self.save_file).grid(column = 1,row = 19)
        self.button_quit = Button(master, text = 'Exit', fg = 'white', bg = master['bg'], height = 3, width = 20, command = lambda: self.check_quit(master)).grid(column = 3,row = 19)
        self.button_upload = Button(master, text = 'Upload coordinates', fg = 'white', bg = master['bg'], height = 3, width = 20, command = self.upload_sa).grid(column = 0, row = 19)
        self.button_reset = Button(master, text = 'Reset', fg = 'white', bg = master['bg'], height = 3, width = 20, command = self.reset).grid(column = 2, row = 19)
