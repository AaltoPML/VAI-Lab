from . import UI

import tkinter as tk                # python 3
import os
from PIL import Image, ImageTk

from tkinter import messagebox, ttk

from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
import numpy as np
import pandas as pd

class PageCanvas(tk.Frame,UI):
    def __init__(self, parent, controller):
        super().__init__(parent, bg = parent['bg'])
        self.controller = controller
        self.controller.title('Canvas Input')
        
        # Create a canvas widget
        self.width, self.height = 600, 600
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, background="white")

        self.canvas.grid(row=0, column=0, columnspan=4, rowspan = 2)
        # self.checkered(10)

        self.canvas.bind('<Button-1>', self.draw_dot)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        # #linux scroll
        # self.canvas.bind("<Button-4>", self.zoomerP)
        # self.canvas.bind("<Button-5>", self.zoomerM)
        # #windows scroll
        # self.canvas.bind("<MouseWheel>",self.zoomer)
        

        # Booleans to identify what the user wants to do
        self.draw = tk.StringVar()
        self.draw.set('draw')
        self.state = tk.StringVar()
        self.state.set('state')

        # Buttons under the canvas
        self.button_draw = tk.Radiobutton(self,
                                            text = 'Draw', 
                                            fg = 'white',
                                            bg = parent['bg'], 
                                            height = 3,
                                            width = 20, 
                                            var = self.draw,
                                            selectcolor = 'black',
                                            value = 'draw'
                                            ).grid(column = 4,row = 3)
        self.button_drag = tk.Radiobutton(self,
                                            text = 'Move',
                                            fg = 'white',
                                            bg = parent['bg'],
                                            height = 3, 
                                            width = 20,
                                            var = self.draw,
                                            selectcolor = 'black',
                                            value = 'drag'
                                            ).grid(column = 5,row = 3)
        self.button_edit = tk.Radiobutton(self,
                                            text = 'Edit',
                                            fg = 'white',
                                            bg = parent['bg'],
                                            height = 3, 
                                            width = 20,
                                            var = self.draw, 
                                            selectcolor = 'black',
                                            value = 'edit'
                                            ).grid(column = 6,row = 3)
        self.button_save = tk.Button(self,
                                            text = 'Save',
                                            fg = 'white',
                                            bg = parent['bg'],
                                            height = 3, 
                                            width = 20,
                                            command = self.save_file
                                            ).grid(column = 1,row = 3)
        self.button_upload = tk.Button(self,
                                            text = 'Upload coordinates',
                                            fg = 'white',
                                            bg = parent['bg'],
                                            height = 3,
                                            width = 20,
                                            command = self.upload_sa
                                            ).grid(column = 0, row = 3)
        self.button_reset = tk.Button(self, 
                                            text = 'Reset',
                                            fg = 'white',
                                            bg = parent['bg'],
                                            height = 3, 
                                            width = 20,
                                            command = self.reset
                                            ).grid(column = 2, row = 3)
        if self.controller.startpage_exist:
            self.button_main = tk.Button(self, 
                                                text="Go to the main page",
                                                fg = 'white',
                                                bg = parent['bg'], 
                                                height = 3, 
                                                width = 20,
                                                command = self.check_quit
                                                ).grid(column = 3, row = 3)

        #Tree defintion. Output display
        style = ttk.Style()
        style.configure("Treeview",
                            background = 'white', 
                            foreground = 'white',
                            rowheight = 25, 
                            fieldbackground = 'white',
                            font = self.controller.pages_font)
        style.configure("Treeview.Heading",
                            font = self.controller.pages_font)
        style.map('Treeview', 
                            background = [('selected', 'grey')])
        

        tree_frame = tk.Frame(self)
        tree_frame.grid(row = 0,
                        column = 4,
                        columnspan = 3,
                        rowspan = 2)
        
        tree_scrollx = tk.Scrollbar(tree_frame, orient = 'horizontal')
        tree_scrollx.pack(side = tk.BOTTOM, fill = tk.X)
        tree_scrolly = tk.Scrollbar(tree_frame)
        tree_scrolly.pack(side = tk.RIGHT, fill = tk.Y)
        
        self.tree = ttk.Treeview(tree_frame,
                                    yscrollcommand = tree_scrolly.set,
                                    xscrollcommand = tree_scrollx.set
                                    )
        self.tree.pack()
        
        tree_scrollx.config(command = self.tree.xview)
        tree_scrolly.config(command = self.tree.yview)
        
        self.save_path = ''
        self.saved = True

    def class_list(self):
        """Getter for required _class_list variable
        
        :return: list of class labels
        :rtype: list of strings
        """
        return self._class_list

    def class_list(self,value):
        """Setter for required _class_list variable
        
        :param value: labels for state-action pair headers
        :type value: list of strings
        """
        self._class_list = value
        # self.out_data = {'State_x': [], 'State_y': [], 'Action_x': [], 'Action_y': []} #coordinates
        self.out_data = {out: [] for out in self._class_list} #coordinates
        self.tree['columns'] = self._class_list
        
        
        # Format columns
        self.tree.column("#0", width = 50)
        for n, cl in enumerate(self._class_list):
            self.tree.column(cl,
                            width = int(self.controller.pages_font.measure(str(cl)))+20,
                            minwidth = 50,
                            anchor = tk.CENTER
                            )
                
        # Headings
        self.tree.heading("#0", text = "Sample", anchor = tk.CENTER)
        for cl in self._class_list:
            self.tree.heading(cl, text = cl, anchor = tk.CENTER)
        
        # Define double-click on row action
        self.tree.bind("<Double-1>", self.OnDoubleClick)

    def draw_dot(self, event):    
        
        if self.draw.get() == 'drag':
            selected = self.canvas.find_overlapping(event.x-10,
                                                    event.y-10,
                                                    event.x+10,
                                                    event.y+10
                                                    )
            if selected:
                self.canvas.selected = selected[0]  # select the top-most item
                self.canvas.startxy = (event.x, event.y)
            else:
                self.canvas.selected = None

        if self.draw.get()  == 'draw':

            # Draw an oval in the given coordinates
            self.saved = False
            if self.state.get()  == 'state': # Write state coordinates
                self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black", width=0, 
                                        tags=("state-" + str(len(self.out_data['State_x']))))
                self.out_data['State_x'].append(event.x)
                self.out_data['State_y'].append(event.y)
                self.state.set('action')
                if self.tree.selection(): # Update coordinates in corresponding row if exists.
                    n = int(self.tree.selection()[0]) + 1
                    self.tree.insert(parent = '', index = 'end', iid = n, text = n+1, 
                                     values = tuple(self.dict2mat(self.out_data)[n,:].astype(int)))
                    self.tree.selection_set(str(n))
                else:
                    self.tree.insert(parent = '', index = 'end', iid = 0, text = 1, 
                                     values = tuple(self.dict2mat(self.out_data)[0,:].astype(int)))
                    self.tree.selection_set(str(0))
                
            elif self.state.get()  == 'action':
                self.canvas.create_line(self.out_data['State_x'][-1], self.out_data['State_y'][-1], event.x, event.y, 
                                        fill="red", arrow=tk.LAST, tags=("action-" + str(len(self.out_data['Action_x']))))
                self.out_data['Action_x'].append(event.x)
                self.out_data['Action_y'].append(event.y)
                self.state.set('state')
                n = int(self.tree.selection()[0])
                self.tree.item(self.tree.get_children()[n], text = n+1, values = tuple(self.dict2mat(self.out_data)[n,:].astype(int)))


    def on_drag(self, event):
        if self.draw.get()  == 'drag' and self.canvas.selected:
            # calculate distance moved from last position
            dx, dy = event.x - self.canvas.startxy[0], event.y - self.canvas.startxy[1]
            # move the selected item
            print(self.canvas.gettags("current"))
            n = int(self.canvas.gettags("current")[0].split('-')[1])
            # If state, updates both the state placement and the arrow
            if self.canvas.gettags("current")[0].split('-')[0] == 'state':
                self.canvas.move(self.canvas.selected, dx, dy)
                self.canvas.coords('action-'+str(n), (event.x, event.y, self.out_data['Action_x'][n], 
                                                                       self.out_data['Action_y'][n]))
                self.out_data['State_x'][n] = event.x
                self.out_data['State_y'][n] = event.y  
            elif self.canvas.gettags("current")[0].split('-')[0] == 'action': # If action, updates the arrow end of the line position
                self.canvas.coords(self.canvas.gettags("current")[0], (self.out_data['State_x'][n], 
                                                                       self.out_data['State_y'][n], event.x, event.y))
                self.out_data['Action_x'][n] = event.x
                self.out_data['Action_y'][n] = event.y
            # update last position
            self.canvas.startxy = (event.x, event.y)                
            self.tree.item(self.tree.get_children()[n], text = n+1, 
                           values = tuple(self.dict2mat(self.out_data)[n,:].astype(int)))
            self.tree.selection_set(str(n))
            
    def checkered(self, line_distance):        
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, self.width, line_distance):
            self.canvas.create_line(x, 0, x, self.height, fill="#476042")
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance, self.height, line_distance):
            self.canvas.create_line(0, y, self.width, y, fill="#476042")   
            
    def check_quit(self):
        if self.saved:
            self.controller.show_frame("StartPage")
        else:
            response = messagebox.askokcancel("Are you sure you want to leave?", "Do you want to leave the program without saving?")
            if response:
                self.controller.show_frame("StartPage")
            
            
    def save_file_as(self):
        self.save_path = asksaveasfile(mode='w')
        self.save_file()
        
    def save_file(self):
        if self.save_path == '':
            self.save_path = asksaveasfile(defaultextension = '.txt', filetypes = [('Text file', '.txt'), ('CSV file', '.csv'), ('All Files', '*.*')])
        if self.save_path is not None: # asksaveasfile return `None` if dialog closed with "cancel".

            filedata = pd.DataFrame(self.out_data, columns = ['State_x', 'State_y', 'Action_x', 'Action_y']).to_string()

            self.save_path.seek(0) # Move to the first row to overwrite it
            self.save_path.write(filedata)
            self.save_path.flush() # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(self.save_path.fileno())
            self.saved = True
            
    def OnDoubleClick(self, event):
        "Moves to the image corresponding to the row clicked on the tree."
        
        print('What to do?...')
        # item = self.tree.selection()[0]
        # self.canvas.itemconfig("state-"+str(item), fill="blue")
        
        
        
    def upload_sa(self):
        filename = askopenfilename(initialdir = os.getcwd(), title = 'Select a file', defaultextension = '.txt', filetypes = [('Text file', '.txt'), ('CSS file', '.css'), ('All Files', '*.*')])
        if filename is not None:
            data = open(filename,'r')
            read = False
            self.draw.set('drag')

            for n, point in enumerate(data):
                if read: # Not elegant at all, just to omit the header.
                    i, sx, sy, ax, ay = point.split()
                    # Draw an oval in the given coordinates
                    self.canvas.create_oval(float(sx)-3, float(sy)-3, float(sx)+3, float(sy)+3, fill="black", width=0, 
                                            tags=("state-" + str(len(self.out_data['State_x']))))
                    self.canvas.create_line(float(sx), float(sy), float(ax), float(ay), fill="red", arrow=tk.LAST, 
                                            tags=("action-" + str(len(self.out_data['Action_x']))))
                    self.out_data['State_x'].append(sx)
                    self.out_data['State_y'].append(sy)
                    self.out_data['Action_x'].append(ax)
                    self.out_data['Action_y'].append(ay)
                    self.tree.insert(parent = '', index = 'end', iid = len(self.out_data['Action_x'])-1, text = len(self.out_data['Action_x']), 
                                      values = tuple(self.dict2mat(self.out_data)[len(self.out_data['Action_x'])-1,:].astype(int)))
                    self.tree.selection_set(str(len(self.out_data['Action_x'])-1))

                else:
                    read = True
    def reset(self):
        msg = messagebox.askyesnocancel('Info', 'Are you sure you want to reset the canvas?')
        if msg:
            self.canvas.delete(tk.ALL)
            # self.checkered(10)
            self.out_data = dict.fromkeys(self._class_list,[]) #coordinates
            for record in self.tree.get_children():
                self.tree.delete(record)

            
    #windows zoom
    def zoomer(self, event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerM(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        

    def dict2mat(self, X):
        max_size = 0
        for key in X:
            if len(X[key]) > max_size:
                max_size = len(X[key])

        result = -np.ones((max_size, len(X)))
        for k, key in enumerate(X):
            result[:len(X[key]), k]  = X[key]
            
        return result