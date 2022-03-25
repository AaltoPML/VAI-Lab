# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 11:47:53 2022

@author: Sevisal
"""

import tkinter as tk                # python 3
import os
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
import numpy as np
import pandas as pd
import math


class PageManual(tk.Frame):
    
    
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
            result = Image.new(pil_img.mode, (height, height), 
                               background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result

    def check_quit(self):
        
        global saved
        if not saved:
            response = messagebox.askokcancel(
                "Are you sure you want to leave?", 
                "Do you want to leave the program without saving?")
            if response:
                self.controller.show_frame("StartPage")
        else:
            self.controller.show_frame("StartPage")
    
    def open_file(self):
        
        global save_path
        save_path = askopenfile(mode='r+')
        if save_path is not None:
            t = save_path.read()
            # textentry.delete('0.0', 'end')
            # textentry.insert('0.0', t)
            # textentry.focus()
            
    def save_file_as(self):
        
        global save_path
        save_path = asksaveasfile(mode='w')
        self.save_file()
        
    def save_file(self):
        
        global save_path
        global saved
        if save_path == '':
            save_path = asksaveasfile(defaultextension = '.txt', 
                                      filetypes = [('Text file', '.txt'), 
                                                   ('CSV file', '.csv'), 
                                                   ('All Files', '*.*')])
        if save_path is not None: # asksaveasfile return `None` if dialog closed with "cancel".
            filedata = pd.DataFrame(
                self.out_data, columns = self.class_list).to_string()
            save_path.seek(0) # Move to the first row to overwrite it
            save_path.write(filedata)
            save_path.flush() # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(save_path.fileno())
            saved = True
            
    def forward_back(self, image_number):
        
        " Forward button to continue to the next image in the folder."
        
        self.tree.selection_set(str(int(image_number-1)))
        # Print the corresponding image
        self.my_label.grid_forget()
        self.my_label = tk.Label(self, image=self.image_list[image_number-1])
        
        # Update button commands
        self.button_forw = tk.Button(
            self, image = self.forw_img, bg = self.parent['bg'], 
            command = lambda: self.forward_back(
                image_number+1)).grid(column = 2,row = 19)
        self.button_back = tk.Button(
            self, image = self.back_img, bg = self.parent['bg'], 
            command = lambda: self.forward_back(
                image_number-1)).grid(column = 0,row = 19)
        if image_number == self.N:
            self.button_forw = tk.Button(
                self, image = self.forw_img, bg = self.parent['bg'], 
                state = tk.DISABLED).grid(column = 2,row = 19)
        if image_number == 1:
            self.button_back = tk.Button(
                self, image = self.back_img, bg = self.parent['bg'], 
                state = tk.DISABLED).grid(column = 0,row = 19)
            
        self.my_label.grid(column=0, row=0, rowspan = 10, columnspan=3)
        
        # Classes buttons
        # var = {}
        for i,cl in enumerate(self.class_list):
            # print(out_data[image_number-1,i])
            self.var[image_number-1,i] = tk.IntVar(
                value = int(self.out_data[image_number-1,i]))
            # var[i] = tk.IntVar(value = int(self.out_data[image_number-1,i]))
            # I can not make this be selected when going backwards or forward if it was previously selected.
            self.button_cl[cl] = tk.Checkbutton(
                self, text = cl, fg = 'white', bg = self.parent['bg'], 
                selectcolor = 'black', height = 3, width = 20, 
                variable = self.var[image_number-1,i], 
                command=(lambda i=i: self.onPress(image_number-1,i)))
            self.button_cl[cl].grid(column = 4,row = i)

        # Status bar    
        status = tk.Label(
            self, text='Image ' + str(image_number) + ' of '+str(self.N), 
            bd = 1, relief = tk.SUNKEN, anchor = tk.E, fg = 'white', 
            bg = self.parent['bg'])
        status.grid(row=20, column=0, columnspan=4, pady = 10, 
                    sticky = tk.W+tk.E)
            
    def onPress(self, n,i):
        
        "Updates the stored values on clicking the checkbutton."
        
        global saved              
        self.out_data[n,i] = not self.out_data[n,i]
        self.tree.item(self.tree.get_children()[n], text = n+1, 
                       values = tuple(self.out_data[n,:].astype(int)))
        saved = False
        
    def OnDoubleClick(self, event):
        
        "Moves to the image corresponding to the row clicked on the tree."
        
        item = self.tree.selection()[0]
        self.forward_back(self.tree.item(item,"text"))

    def __init__(self, parent, controller):
        
        super().__init__(parent, bg = parent['bg'])
        self.controller = controller
        self.parent = parent
        
        dirpath = os.getcwd()
        
        self.class_list = ['Atelectasis', 'Cardiomelagy', 'Effusion', 
                           'Infiltration', 'Mass', 'Nodule', 'Pneumonia', 
                           'Pneumothorax'
                           ]
        
        pixels = 500
        path = os.path.join(dirpath, 'Example_images')
        self.N = len(os.listdir(path))
        
        # Create a list with all the available (I have tried reading the file when placing it but wasn't able to)
        self.image_list = []
        for f in os.listdir(path):
            self.image_list.append(
                ImageTk.PhotoImage(self.expand2square(
                    Image.open(os.path.join(path, f)), 
                    (0, 0, 0)).resize((pixels, pixels)))) # (0, 0, 0) is the padding colour
        
        # Status bar in the lower part of the window
        status = tk.Label(self, text='Image 1 of '+str(self.N), bd = 1, 
                          relief = tk.SUNKEN, anchor = tk.E, fg = 'white', 
                          bg = parent['bg'])
        status.grid(row=20, column=0, columnspan=4, pady = 10, 
                    sticky = tk.W+tk.E)
        
        # Inital window
        self.my_label = tk.Label(self, image = self.image_list[0], 
                                 bg = parent['bg'])
        self.my_label.grid(column = 0, row = 0, rowspan = 10, columnspan = 3)
    
        # Buttons initialisation
        self.back_img = ImageTk.PhotoImage(Image.open(
            dirpath+'\\Icons\\back_arrow.png').resize((150, 50)))
        self.forw_img = ImageTk.PhotoImage(Image.open(
            dirpath+'\\Icons\\forw_arrow.png').resize((150, 50)))
        self.button_back = tk.Button(
            self, image = self.back_img, bg = parent['bg'], 
            state = tk.DISABLED).grid(column = 0,row = 19)
        self.button_save = tk.Button(
            self, text = 'Save', fg = 'white', bg = parent['bg'], height = 3, 
            width = 20, command = self.save_file).grid(column = 1,row = 19)
        self.button_forw = tk.Button(
            self, image = self.forw_img, bg = parent['bg'], 
            command = lambda: self.forward_back(2)).grid(column = 2,row = 19)
        
        button_main = tk.Button(
            self, text="Go to the main page", 
            fg = 'white', bg = parent['bg'], height = 3, width = 20, 
            command = self.check_quit).grid(column = 4,row = 19)
        
        self.out_data = np.zeros((self.N, len(self.class_list)))
        self.button_cl = {}
        
        self.var = {}
        for i,cl in enumerate(self.class_list):
            self.var[0,i] = tk.IntVar(value=self.out_data[0,i])
            self.button_cl[cl] = tk.Checkbutton(
                self, text = cl, fg = 'white', bg = parent['bg'], 
                selectcolor = 'black', height = 3, width = 20, 
                variable = self.var[0,i], 
                command=(lambda i=i: self.onPress(0,i)))
            self.button_cl[cl].grid(column = 4,row = i)
        
        #Tree defintion. Output display
        style = ttk.Style()
        style.configure(
            "Treeview", background = 'white', foreground = 'black', 
            rowheight = 25, fieldbackground = 'white', 
            font = self.controller.pages_font)
        style.configure("Treeview.Heading", font = self.controller.pages_font)
        style.map('Treeview', background = [('selected', 'blue')])
        

        tree_frame = tk.Frame(self)
        tree_frame.grid(row = 0, column = 5, columnspan = 4, rowspan = 10)
        
        tree_scrollx = tk.Scrollbar(tree_frame, orient = 'horizontal')
        tree_scrollx.pack(side = tk.BOTTOM, fill = tk.X)
        tree_scrolly = tk.Scrollbar(tree_frame)
        tree_scrolly.pack(side = tk.RIGHT, fill = tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, 
                                 yscrollcommand = tree_scrolly.set, 
                                 xscrollcommand = tree_scrollx.set)
        self.tree.pack()
        
        tree_scrollx.config(command = self.tree.xview)
        tree_scrolly.config(command = self.tree.yview)
        
        self.tree['columns'] = self.class_list
        
        # Format columns
        self.tree.column("#0", width = 50)
        for n, cl in enumerate(self.class_list):
            self.tree.column(
                cl, width = int(self.controller.pages_font.measure(str(cl)))+20, 
                minwidth = 50, anchor = tk.CENTER)
                
        # Headings
        self.tree.heading("#0", text = "Image", anchor = tk.CENTER)
        for cl in self.class_list:
            self.tree.heading(cl, text = cl, anchor = tk.CENTER)
            
        # Add data
        for n, sample in enumerate(self.out_data):
            self.tree.insert(parent = '', index = 'end', iid = n, text = n+1, 
                             values = tuple(sample.astype(int)))
        
        # Select the current row
        self.tree.selection_set(str(int(0)))
        
        # Define double-click on row action
        self.tree.bind("<Double-1>", self.OnDoubleClick)

# class writen_mlbl:
#     def __init__(self, master):
#         messagebox.showwarning("Error", "This functionality is not yet implemented.")
        
# class speak_mlbl:
#     def __init__(self, master):
#         messagebox.showwarning("Error", "This functionality is not yet implemented.")     
        
# class upload_mlbl:
#     def __init__(self, master):
#         master.filename = askopenfilename(initialdir = os.getcwd(), title = 'Select a file', defaultextension = '.txt', filetypes = [('Text file', '.txt'), ('CSS file', '.css'), ('All Files', '*.*')])
#         if master.filename is not None:
#             messagebox.showinfo("Success", "Feedback correctly uploaded.")


class PageCanvas(tk.Frame):

    
    global save_path
    global saved
    global selected
    save_path = ''
    saved = True
        
    def draw_dot(self, event):
        
        ii = self.notebook.index(self.notebook.select())
        if self.draw[ii].get() == 'drag':
            selected = self.canvas[ii].find_overlapping(event.x-10, event.y-10, 
                                                        event.x+10, event.y+10)
            if selected:
                self.canvas[ii].selected = selected[0]  # select the top-most item
                self.canvas[ii].startxy = (event.x, event.y)
            else:
                self.canvas[ii].selected = None

        if self.draw[ii].get()  == 'draw':
            # Draw an oval in the given coordinates
            global saved
            saved = False
            # Angle of the selected point with respect to the circle center
            if self.type[ii] == 'Rotating':
                alpha = np.arctan((event.y-self.y_ini)/(event.x-self.x_ini)) 
                alpha += ((event.x - self.x_ini) < 0) * math.pi
                x_o = self.r * np.cos(alpha) + self.x_ini
                y_o = self.r * np.sin(alpha) + self.y_ini
                if self.state[ii].get()  == 'state': # Write state coordinates
                    self.canvas[ii].create_oval(
                        x_o-3, y_o-3, x_o+3, y_o+3, fill="black", width=0, 
                        tags=("state"+str(ii)+'-'
                              + str(len(self.out_data[ii]['State_a']))))
                    self.out_data[ii]['State_a'].append((
                        -np.rad2deg(alpha)+360)%360)
                    self.state[ii].set('action')
                    if self.tree[ii].selection(): # Update coordinates in corresponding row if exists.
                        n = int(self.tree[ii].selection()[0]) + 1
                        self.tree[ii].insert(
                            parent = '', index = 'end', iid = n, text = n+1, 
                            values = tuple(self.dict2mat(
                                self.out_data[ii])[n,:].astype(int)))
                        self.tree[ii].selection_set(str(n))
                    else:
                        self.tree[ii].insert(
                            parent = '', index = 'end', iid = 0, text = 1, 
                            values = tuple(self.dict2mat(
                                self.out_data[ii])[0,:].astype(int)))
                        self.tree[ii].selection_set(str(0))
                    
                elif self.state[ii].get()  == 'action':
                    if (self.out_data[ii]['State_a'][-1] 
                        - (-np.rad2deg(alpha)+360)%360)%180 > 0:
                        self.create_circle_arc(
                            self.x_ini, self.y_ini, self.r, fill = "", 
                            outline = "red", start = 
                            self.out_data[ii]['State_a'][-1], end = 
                            np.rad2deg(-alpha), width=2, style = tk.ARC, 
                            tags=("action"+str(ii)+'-'+ str(len(
                                self.out_data[ii]['State_a']))))
                    else:
                        self.create_circle_arc(
                            self.x_ini, self.y_ini, self.r, fill = "", 
                            outline = "red", start = np.rad2deg(-alpha), 
                            end = self.out_data[ii]['State_a'][-1], width=2, 
                            style = tk.ARC)                   
                    self.out_data[ii]['Action_a'].append((
                        -np.rad2deg(alpha)+360)%360)
                    self.state[ii].set('state')
                    n = int(self.tree[ii].selection()[0])
                    self.tree[ii].item(
                        self.tree[ii].get_children()[n], text = n+1, 
                        values = tuple(self.dict2mat(
                            self.out_data[ii])[n,:].astype(int)))
            else:
                if self.state[ii].get()  == 'state': # Write state coordinates
                    self.canvas[ii].create_oval(
                        event.x-3, event.y-3, event.x+3, event.y+3, 
                        fill="black", width=0, 
                        tags=("state"+str(ii)+'-'+ str(len(
                            self.out_data[ii]['State_x']))))
                    self.out_data[ii]['State_x'].append(event.x)
                    self.out_data[ii]['State_y'].append(event.y)
                    self.state[ii].set('action')
                    if self.tree[ii].selection(): # Update coordinates in corresponding row if exists.
                        n = int(self.tree[ii].selection()[0]) + 1
                        self.tree[ii].insert(
                            parent = '', index = 'end', iid = n, text = n+1, 
                            values = tuple(self.dict2mat(
                                self.out_data[ii])[n,:].astype(int)))
                        self.tree[ii].selection_set(str(n))
                    else:
                        self.tree[ii].insert(
                            parent = '', index = 'end', iid = 0, text = 1, 
                            values = tuple(self.dict2mat(
                                self.out_data[ii])[0,:].astype(int)))
                        self.tree[ii].selection_set(str(0))
                    
                elif self.state[ii].get()  == 'action':
                    self.canvas[ii].create_line(
                        self.out_data[ii]['State_x'][-1], 
                        self.out_data[ii]['State_y'][-1], event.x, event.y, 
                        fill="red", arrow=tk.LAST, 
                        tags=("action"+str(ii)+'-' + str(len(
                            self.out_data[ii]['Action_x']))))
                    self.out_data[ii]['Action_x'].append(event.x)
                    self.out_data[ii]['Action_y'].append(event.y)
                    self.state[ii].set('state')
                    n = int(self.tree[ii].selection()[0])
                    self.tree[ii].item(
                        self.tree[ii].get_children()[n], text = n+1, 
                        values = tuple(self.dict2mat(
                            self.out_data[ii])[n,:].astype(int)))                

    def on_drag(self, event):
        
        ii = self.notebook.index(self.notebook.select())
        if self.draw[ii].get()  == 'drag' and self.canvas[ii].selected:
            # move the selected item
            n = int(self.canvas[ii].gettags("current")[0].split('-')[1])
            
            if self.type[ii] == 'Rotating':
                alpha = np.arctan((event.y-self.y_ini)/(event.x-self.x_ini))
                +((event.x-self.x_ini) < 0) * math.pi
                dx = self.r * np.cos(alpha) + self.x_ini
                dy = self.r * np.sin(alpha) + self.y_ini
                if self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'state'+str(ii): # If state, updates both the state placement and the arrow
                    self.canvas[ii].move(
                        self.canvas[ii].selected, dx-self.canvas[ii].startxy[0], 
                        dy - self.canvas[ii].startxy[1])
                    self.canvas[ii].coords(
                        "action"+str(ii)+'-'+str(n), 
                        (event.x, event.y, self.out_data[ii]['Action_x'][n],
                         self.out_data[ii]['Action_y'][n]))
                    self.out_data[ii]['State_a'][n] = alpha
                elif self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'action'+str(ii): # If action, updates the arrow end of the line position
                    self.canvas[ii].coords(
                        self.canvas[ii].gettags("current")[0], 
                        (self.out_data[ii]['State_x'][n], 
                        self.out_data[ii]['State_y'][n], event.x, event.y))
                    self.out_data[ii]['Action_x'][n] = event.x
                    self.out_data[ii]['Action_y'][n] = event.y               
            else:
                # calculate distance moved from last position
                dx = event.x - self.canvas[ii].startxy[0]
                dy = event.y - self.canvas[ii].startxy[1]
                if self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'state'+str(ii): # If state, updates both the state placement and the arrow
                    self.canvas[ii].move(self.canvas[ii].selected, dx, dy)
                    self.canvas[ii].coords(
                        "action"+str(ii)+'-'+str(n), 
                        (event.x, event.y, self.out_data[ii]['Action_x'][n], 
                        self.out_data[ii]['Action_y'][n]))
                    self.out_data[ii]['State_x'][n] = event.x
                    self.out_data[ii]['State_y'][n] = event.y  
                elif self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'action'+str(ii): # If action, updates the arrow end of the line position
                    self.canvas[ii].coords(
                        self.canvas[ii].gettags("current")[0], 
                        (self.out_data[ii]['State_x'][n], 
                         self.out_data[ii]['State_y'][n], event.x, event.y))
                    self.out_data[ii]['Action_x'][n] = event.x
                    self.out_data[ii]['Action_y'][n] = event.y
            # update last position
            self.canvas[ii].startxy = (event.x, event.y)                
            self.tree[ii].item(self.tree[ii].get_children()[n], text = n+1, 
                           values = tuple(self.dict2mat(
                               self.out_data[ii])[n,:].astype(int)))
            self.tree[ii].selection_set(str(n))

    def checkered(self, line_distance):
        
        ii = self.notebook.index(self.notebook.select()) 
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, self.width, line_distance):
            self.canvas[ii].create_line(x, 0, x, self.height, fill="#476042")
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance, self.height, line_distance):
            self.canvas[ii].create_line(0, y, self.width, y, fill="#476042")   
            
    def check_quit(self):
        
        global saved
        if not saved:
            response = messagebox.askokcancel(
                "Are you sure you want to leave?",
                "Do you want to leave the program without saving?")
            if response:
                self.controller.show_frame("StartPage")
        else:
            self.controller.show_frame("StartPage")
            
    def save_file_as(self):
        
        global save_path
        save_path = asksaveasfile(mode='w')
        self.save_file()
        
    def save_file(self):
        
        global save_path
        global saved
        if save_path == '':
            save_path = asksaveasfile(defaultextension = '.txt', filetypes = 
                                      [('Text file', '.txt'), 
                                       ('CSV file', '.csv'), 
                                       ('All Files', '*.*')])
        if save_path is not None: # asksaveasfile return `None` if dialog closed with "cancel".
            # Transform input for output file    
            data = {}
            samples = np.max([len(self.out_data[element][
                list(self.out_data[element].keys())[0]]) 
                for element in self.out_data])
            for ii in self.out_data.keys():
                for c in self.out_data[ii].keys():
                    a, b = c.split('_')
                    aux = self.out_data[ii][c]
                    aux.extend([-1]*(samples - len(self.out_data[ii][c])))
                    data[a+str(ii)+'_'+b] = aux
                    
            filedata = pd.DataFrame(data, columns = data.keys()).to_string()
            save_path.seek(0) # Move to the first row to overwrite it
            save_path.write(filedata)
            save_path.flush() # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(save_path.fileno())
            saved = True
            
    def OnDoubleClick(self, event):
        
        "Moves to the image corresponding to the row clicked on the tree."
        
        print('What to do?...')
        # item = self.tree.selection()[0]
        # self.canvas.itemconfig("state-"+str(item), fill="blue")
        

    def upload_sa(self):
        
        ii = self.notebook.index(self.notebook.select())
        filename = askopenfilename(initialdir = os.getcwd(), 
                                   title = 'Select a file', 
                                   defaultextension = '.txt', 
                                   filetypes = [('Text file', '.txt'), 
                                                ('CSS file', '.css'), 
                                                ('All Files', '*.*')])
        if filename is not None:
            data = open(filename,'r')
            read = False
            self.draw[ii].set('drag')
            for n, point in enumerate(data):
                print(point)
                if read: # Not elegant at all, just to omit the header.
                    i, sx, sy, ax, ay = point.split()
                    # Draw an oval in the given coordinates
                    self.canvas[ii].create_oval(
                        float(sx)-3, float(sy)-3, float(sx)+3, float(sy)+3, 
                        fill="black", width=0, 
                        tags=("state-" + str(len(
                            self.out_data[ii]['State_x']))))
                    self.canvas[ii].create_line(
                        float(sx), float(sy), float(ax), float(ay), 
                        fill="red", arrow=tk.LAST, 
                        tags=("action-" + str(len(
                            self.out_data[ii]['Action_x']))))
                    self.out_data[ii]['State_x'].append(sx)
                    self.out_data[ii]['State_y'].append(sy)
                    self.out_data[ii]['Action_x'].append(ax)
                    self.out_data[ii]['Action_y'].append(ay)
                    self.tree.insert(
                        parent = '', index = 'end', 
                        iid = len(self.out_data[ii]['Action_x'])-1, 
                        text = len(self.out_data[ii]['Action_x']), 
                        values = tuple(self.dict2mat(
                            self.out_data[ii])[len(
                                self.out_data[ii]['Action_x'])-1,:].astype(int)))
                    self.tree.selection_set(str(len(
                        self.out_data[ii]['Action_x'])-1))
                else:
                    read = True
    
    def reset(self):
        
        ii = self.notebook.index(self.notebook.select())
        msg = messagebox.askyesnocancel(
            'Info', 'Are you sure you want to reset the canvas?')
        if msg:
            self.canvas[ii].delete(tk.ALL) # Reset canvas
            self.state[ii].set('state')
            self.out_data[ii] = {}
            for key in self.class_list[ii]:
                self.out_data[ii][key] = []
                    
            for record in self.tree[ii].get_children(): #Reset treeview
                self.tree[ii].delete(record)
            if self.type[ii] == 'Rotating': 
                self.create_circle(self.x_ini, self.y_ini, 4, 
                                   fill="#DDD", outline="", width=4)
                self.create_circle(self.x_ini, self.y_ini, self.r, 
                                   fill="", outline="#DDD", width=4)
    
    def dict2mat(self, X):
        
        max_size = 0
        for key in X:
            if len(X[key]) > max_size:
                max_size = len(X[key])

        result = -np.ones((max_size, len(X)))
        for k, key in enumerate(X):
            result[:len(X[key]), k]  = X[key]
            
        return result
    
    def create_circle(self, x, y, r, **kwargs):
        
        return self.canvas[self.notebook.index(
            self.notebook.select())].create_oval(x-r, y-r, x+r, y+r, **kwargs)
    
    def create_circle_arc(self, x, y, r, **kwargs):
        
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.canvas[self.notebook.index(
            self.notebook.select())].create_arc(x-r, y-r, x+r, y+r, **kwargs)
    
    def __init__(self, parent, controller):
        
        super().__init__(parent, bg = parent['bg'])
        self.controller = controller
        
        # Define the different inputs we want feedback from
        self.class_list = [['State_a', 'Action_a'], 
                           ['State_x', 'State_y', 'Action_x', 'Action_y'], 
                           ['State_x', 'State_y', 'Action_x', 'Action_y']]
        
        self.out_data = {}
        for ii in np.arange(len(self.class_list)):
            self.out_data[ii] = {}
            for key in self.class_list[ii]:
                self.out_data[ii][key] = []
                
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, columnspan=7, 
                           rowspan = 12, pady = 15)
        self.frame = []
        self.tree = []
        self.canvas = []
        self.draw = []
        self.state = []
        self.type = []

        for ii in np.arange(len(self.class_list)):
            self.frame.append(tk.Frame(self, bg = parent['bg']))
            self.frame[-1].grid(row=0, column=0, sticky="nsew", pady = 15)
            if self.class_list[ii][0].split('_')[1] == 'a':
                self.type.append('Rotating')
            else:
                self.type.append('Sliding')
            self.notebook.add(
                self.frame[-1], 
                text = 'Object '+ str(ii) + ' - ' + self.type[-1])
            
            # Create a canvas widget
            self.width, self.height = 600, 600
            self.canvas.append(tk.Canvas(
                self.frame[-1], width=self.width, 
                height=self.height, background="white"))
            self.canvas[-1].grid(row=0, column=0, columnspan=4, rowspan = 2)
            # self.checkered(10)
            self.canvas[-1].bind('<Button-1>', self.draw_dot)
            self.canvas[-1].bind("<B1-Motion>", self.on_drag)
            # self.canvas[-1].bind('<Motion>', self.motion)
            
            # Booleans to identify what the user wants to do
            self.draw.append(tk.StringVar())
            self.draw[ii].set('draw')
            self.state.append(tk.StringVar())
            self.state[ii].set('state')    
            # Buttons under the canvas
            self.button_draw = tk.Radiobutton(
                self.frame[-1], text = 'Draw', fg = 'white', bg = parent['bg'],
                height = 3, width = 20, var = self.draw[ii], 
                selectcolor = 'black', value = 'draw').grid(column = 4,row = 3)
            self.button_drag = tk.Radiobutton(
                self.frame[-1], text = 'Move', fg = 'white', bg = parent['bg'],
                height = 3, width = 20, var = self.draw[ii], 
                selectcolor = 'black', value = 'drag').grid(column = 5,row = 3)
            self.button_edit = tk.Radiobutton(
                self.frame[-1], text = 'Edit', fg = 'white', bg = parent['bg'],
                height = 3, width = 20, var = self.draw[ii], 
                selectcolor = 'black', value = 'edit').grid(column = 6,row = 3)
            self.button_save = tk.Button(
                self.frame[-1], text = 'Save', fg = 'white', bg = parent['bg'],
                height = 3, width = 20, 
                command = self.save_file).grid(column = 1,row = 3)
            self.button_upload = tk.Button(
                self.frame[-1], text = 'Upload coordinates', fg = 'white', 
                bg = parent['bg'], height = 3, width = 20, 
                command = self.upload_sa).grid(column = 0, row = 3)
            self.button_reset = tk.Button(
                self.frame[-1], text = 'Reset', fg = 'white', 
                bg = parent['bg'], height = 3, width = 20, 
                command = self.reset).grid(column = 2, row = 3)
            button_main = tk.Button(
                self.frame[-1], text="Go to the main page", fg = 'white', 
                bg = parent['bg'], height = 3, width = 20,
                command = self.check_quit).grid(column = 3, row = 3)
    
            #Tree defintion. Output display
            style = ttk.Style()
            style.configure(
                "Treeview", background = 'white', foreground = 'white', 
                rowheight = 25, fieldbackground = 'orange', 
                font = self.controller.pages_font)
            style.configure("Treeview.Heading", 
                            font = self.controller.pages_font)
            style.map('Treeview', background = [('selected', 'grey')])
            
    
            tree_frame = tk.Frame(self.frame[-1])
            tree_frame.grid(row = 0, column = 4, columnspan = 3, rowspan = 10)
            
            tree_scrollx = tk.Scrollbar(tree_frame, orient = 'horizontal')
            tree_scrollx.pack(side = tk.BOTTOM, fill = tk.X)
            tree_scrolly = tk.Scrollbar(tree_frame)
            tree_scrolly.pack(side = tk.RIGHT, fill = tk.Y)
            
            self.tree.append(ttk.Treeview(
                tree_frame, 
                yscrollcommand = tree_scrolly.set, 
                xscrollcommand = tree_scrollx.set))
            self.tree[-1].pack()
            
            tree_scrollx.config(command = self.tree[-1].xview)
            tree_scrolly.config(command = self.tree[-1].yview)
            
            if self.type[-1] == 'Rotating':
                self.x_ini, self.y_ini = int(self.width/2), int(self.height/2)
                self.r = int(np.min([self.x_ini, self.y_ini])/1.5)
                self.create_circle(self.x_ini, self.y_ini, 4, 
                                   fill="#DDD", outline="", width=4)
                self.create_circle(self.x_ini, self.y_ini, self.r, 
                                   fill="", outline="#DDD", width=4)
                
            self.tree[-1]['columns'] = self.class_list[ii]
            
            # Format columns
            self.tree[-1].column("#0", width = 50)
            for n, cl in enumerate(self.class_list[ii]):
                self.tree[-1].column(
                    cl, width = int(
                        self.controller.pages_font.measure(str(cl)))+20, 
                    minwidth = 50, anchor = tk.CENTER)
                    
            # Headings
            self.tree[-1].heading("#0", text = "Sample", anchor = tk.CENTER)
            for cl in self.class_list[ii]:
                self.tree[-1].heading(cl, text = cl, anchor = tk.CENTER)
            
            # Define double-click on row action
            self.tree[-1].bind("<Double-1>", self.OnDoubleClick)