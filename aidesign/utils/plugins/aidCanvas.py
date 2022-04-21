# Import the required libraries
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
from tkinter import messagebox

from aidesign.Settings.Settings_core import Settings

class aidCanvas(tk.Frame):

    """ Creates a frame with a canvas and allows to include different modules
    for display which translate into new modules defined for the framework."""
    
    def __init__(self, parent, controller):
        
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        
        super().__init__(parent, bg = parent['bg'])
        self.bg = parent['bg']
        self.controller = controller
        self.controller.title('Assisted Design Display')
        
        self.tk.call('wm','iconphoto', self.controller._w, ImageTk.PhotoImage(
            file = os.path.join(os.path.join(
                os.getcwd(), 'aidesign', 'utils', 'plugins', 
                'resources', 'Assets', 'AIDIcon.ico'))))
        self.my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(
                os.getcwd(), 'aidesign', 'utils', 'plugins', 
                'resources', 'Assets', 'AIDIcon_name.png')).resize((250, 200)))
        
        self.my_label = tk.Label(self, image = self.my_img1, bg = parent['bg'])
        self.my_label.grid(column = 5, row = 0)
        
        # Create canvas
        self.width, self.height = 600, 600
        self.canvas = tk.Canvas(self, width=self.width, 
            height=self.height, background="white")
        self.canvas.grid(row=0, column=0, columnspan=4, rowspan = 10, 
                         padx = 10, pady = 10)
        
        self.canvas.startxy = []
        self.out_data = pd.DataFrame(np.zeros((2,2)), 
                                     columns = ['Initialiser', 'Output'], 
                                     index = ['Initialiser', 'Output'])
        self.connections = {}
        self.connections[0] = {}
        self.connections[1] = {}
        self.module_list = ['Initialiser', 'Output']
        self.module_names = ['Initialiser', 'Output']
        # Create module
        self.w, self.h = 100, 50
        x0 = self.width/2 - (
            self.controller.pages_font.measure('Initialiser')+10)/2

        self.cr = 4
        #Initialiser module
        self.canvas.create_rectangle(x0, self.h, x0 + self.w, 2*self.h, 
                                     tags = 'p0', fill = self.bg, width = 3,
                                     activefill = '#dbaa21')
        self.canvas.create_text(x0 + self.w/2, 3*self.h/2, 
                                text = 'Initialiser', tags = 't0', 
                                fill = '#d0d4d9', 
                                font = self.controller.pages_font)
        self.canvas.create_oval(
                        x0 + self.w/2-self.cr, 2*self.h-self.cr, 
                        x0 + self.w/2+self.cr, 2*self.h+self.cr, 
                        width=2, fill = 'black', tags='d0')
        self.canvas.tag_bind('d0', "<Button-1>", self.join_modules)
        self.canvas.startxy.append((x0 + self.w/2, 
                                    3*self.h/2))
        # Output module
        h_out = self.height - 2*self.h
        self.canvas.create_rectangle(x0, h_out, x0 + self.w, h_out + self.h, 
                                     tags = ('p1'), 
                                     fill = self.bg, width = 3,
                                     activefill = '#dbaa21')
        self.canvas.create_text(x0 + self.w/2, h_out + self.h/2, 
                                text = 'Output', tags = ('t1'), 
                                fill = '#d0d4d9', 
                                font = self.controller.pages_font)
        self.canvas.create_oval(
                        x0 + self.w/2 - self.cr, 
                        h_out - self.cr, 
                        x0 + self.w/2 + self.cr, 
                        h_out  + self.cr,
                        width=2, fill = 'black', tags = ('u1'))
        self.canvas.tag_bind('u1', "<Button-1>", self.join_modules)
        self.canvas.startxy.append((x0 + self.w/2, 
                                    h_out + self.h/2))
        
        self.draw = False
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind('<Button-1>', self.select)
        self.l = 0 #number of loops
        self.drawLoop = False
        self.loops = []
        
        # self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # modules = ['Data preprocessing', 'Modelling', 'Decision making', 'User Feedback Adaptation']
        
        self.modules = 2
        # for m, module in enumerate(modules):
        tk.Button(
            self, text = 'Data processing', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_module('DataProcessing')
            ).grid(column = 5, row = 1)
        tk.Button(
            self, text = 'Modelling', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_module('Modelling')
            ).grid(column = 5, row = 2)
        tk.Button(
            self, text = 'Decision making', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_module('DecisionMaking')
            ).grid(column = 5, row = 3)
        tk.Button(
            self, text = 'User Feedback Adaptation', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_module('UserFeedbackAdaptation')
            ).grid(column = 5, row = 4)
        tk.Button(
            self, text = 'Input data', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_module('InputData')
            ).grid(column = 5, row = 5)
        tk.Button(
            self, text = 'Delete selection', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = self.delete_sel).grid(column = 5, row = 6)
        tk.Button(
            self, text = 'Upload', fg = 'white', bg = parent['bg'], 
            height = 3, width = 20, font = self.controller.pages_font, 
            command = self.upload).grid(column = 0, row = 10, padx = 10)
        tk.Button(
            self, text = 'Save', fg = 'white', bg = parent['bg'],
            height = 3, width = 20, font = self.controller.pages_font, 
            command = self.save_file).grid(column = 1, row = 10)
        tk.Button(
            self, text = 'Reset', fg = 'white', bg = parent['bg'], 
            height = 3, width = 20, font = self.controller.pages_font, 
            command = self.reset).grid(column = 2, row = 10)
        
        self.save_path = ''
        self.saved = True

    def on_return_display(self, event):
            if self.loopDisp:
                condition = self.entry1.get()
                self.entry1.destroy()
                if hasattr(self, 'entry2'):
                    self.entry2.focus()
                key = 'type'
                text_w = self.controller.pages_font.measure(condition) + 20
                x = self.start_x + text_w/2
            else:
                condition = self.entry2.get()
                self.entry2.destroy()
                key = 'condition'
                text_w = self.controller.pages_font.measure(condition) + 20
                x = self.curX - text_w/2
            self.loops[-1][key] = condition
            self.canvas.create_text(
                x, 
                self.start_y + 20, 
                font = self.controller.pages_font, 
                text = condition, 
                tags = ('loop-'+str(self.l-1), key+'-'+str(self.l-1)), 
                justify = tk.CENTER)
            self.canvas.tag_bind(key+'-'+str(self.l-1), 
                             "<Double-1>", self.OnDoubleClick)
            self.loopDisp = not self.loopDisp
    
    def on_button_release(self, event):
        """ Finishes drawing the rectangle for loop definition. 
            Once the rectangle is drawn, it stores the information of the 
            modules inside the loop.
        """
        if self.drawLoop:
            self.drawLoop = False
            
            if (abs(self.start_x - self.curX) > 10) and (
                    abs(self.start_y - self.curY) > 10):
                self.l += 1
                # Identify modules in area
                loopMod = self.canvas.find_enclosed(self.start_x, self.start_y, 
                                                    self.curX, self.curY)
                self.loops.append({'type': None,
                                   'condition': None,
                                   'mod': [], 
                                   'coord': (self.start_x, self.start_y, 
                                             self.curX, self.curY)})
                for mod in loopMod:
                    aux = self.canvas.itemcget(mod, 'tags').split(' ')[1]
                    if len(aux) == 2 and aux[0] == 't':
                        self.loops[-1]['mod'].append(self.canvas.itemcget(
                            mod, 'text'))
                
                # Ask for loop definition and condition and display               
                self.entry1 = tk.Entry(self.canvas, justify='center', 
                                      font = self.controller.pages_font)
                text = 'For/While'
                self.loopDisp = True
                self.entry1.insert(0, text)
                # self.entry['selectbackground'] = '#d0d4d9'
                self.entry1['exportselection'] = False
        
                self.entry1.focus()
                self.entry1.bind("<Return>", self.on_return_display)
                self.entry1.bind("<Escape>", lambda *ignore: self.entry1.destroy())
                
                self.entry1.place(
                    x = self.start_x + 10,
                    y = self.start_y + 20, 
                    anchor = tk.W,
                    width = self.controller.pages_font.measure(text)+10)
                text = 'Condition'
                self.entry2 = tk.Entry(self.canvas, justify='center', 
                                      font = self.controller.pages_font)
                self.entry2.insert(0, text)
                self.entry2['exportselection'] = False
        
                self.entry2.bind("<Return>", self.on_return_display)
                self.entry2.bind("<Escape>", lambda *ignore: self.entry.destroy())
                
                self.entry2.place(
                    x = self.curX-self.controller.pages_font.measure(text)-20,
                    y = self.start_y + 20, 
                    anchor = tk.W,
                    width = self.controller.pages_font.measure(text)+10)
                
                self.saved = False
            else:
                self.canvas.delete('loop-'+str(self.l))
        else:
            self.updateLoops()
    
    def updateLoops(self):
        """ Checks if, after some movement, a module is included in an existing
            loop
        """
        for l, loop in enumerate(self.loops):
            coord = loop['coord']
            loopMod = self.canvas.find_enclosed(coord[0], coord[1],
                                                coord[2], coord[3])
            self.loops[l]['mod'] = []
            for mod in loopMod:
                aux = self.canvas.itemcget(mod, 'tags').split(' ')[1]
                if len(aux) == 2 and aux[0] == 't':
                    self.loops[l]['mod'].append(self.canvas.itemcget(
                        mod, 'text'))
        print('Updated loop info:', self.loops)
        
    def select(self, event):
        """ Selects the module at the mouse location. """
        self.selected = self.canvas.find_overlapping(
            event.x-5, event.y-5, event.x+5, event.y+5)
        if self.selected:
            if len(self.selected) > 2:
                self.canvas.selected = self.selected[-2]
            else:
                self.canvas.selected = self.selected[-1]
            # self.canvas.startxy = (event.x, event.y)
        else:
            self.canvas.selected = None
            # save mouse drag start position
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)
            self.curX = self.start_x
            self.curY = self.start_y
            self.selected = self.canvas.find_overlapping(
                        event.x-5, event.y-5, event.x+5, event.y+5)
    
            # create rectangle if not yet exist
            if not self.selected:
                self.rect = self.canvas.create_rectangle(event.x, event.y, 
                                             event.x, event.y, 
                                             outline = '#4ff07a',
                                             tag = 'loop-'+str(self.l))
                                             # ,fill = '#b3ffc7')
                self.drawLoop = True
                if self.l == 0:
                    self.canvas.tag_lower('loop-'+str(self.l))
                else:
                    self.canvas.tag_raise('loop-'+str(self.l), 'loop-'+str(self.l-1))
        
        if len(self.canvas.gettags("current")) > 0:
            if(len(self.canvas.gettags("current")[0].split('-')) > 1) and (
                self.canvas.gettags("current")[0].split('-')[0] == 'loop'):
                self.isLoop = True
                self.m = int(self.canvas.gettags("current")[0].split('-')[1])
            else:
                self.isLoop = False
                self.m = int(self.canvas.gettags("current")[0][1:])
    
    def on_drag(self, event):
        """ Uses the mouse location to move the module and its text. 
        At the same time, it looks up if there are any connection to this
        module and subsequently moves the connection."""
        
        if self.drawLoop:
            self.curX = self.canvas.canvasx(event.x)
            self.curY = self.canvas.canvasy(event.y)
    
            # w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            # if event.x > 0.9*w:
            #     self.canvas.xview_scroll(1, 'units') 
            # elif event.x < 0.1*w:
            #     self.canvas.xview_scroll(-1, 'units')
            # if event.y > 0.9*h:
            #     self.canvas.yview_scroll(1, 'units') 
            # elif event.y < 0.1*h:
            #     self.canvas.yview_scroll(-1, 'units')
    
            # expand rectangle as you drag the mouse
            self.canvas.coords('loop-'+str(self.l), self.start_x, 
                               self.start_y, self.curX, self.curY)
        else:
            self.select(event)
            
            self.m = int(self.canvas.gettags("current")[0][1:])
            dx = event.x - self.canvas.startxy[self.m][0]
            dy = event.y - self.canvas.startxy[self.m][1]
            # if self.isLoop:
                # self.canvas.move('loop-'+str(self.m), dx, dy) 
            # else:
            # module
            self.canvas.move('o'+str(self.m), dx, dy)
            # self.updateLoops()
            # Connections
            if any(self.out_data.iloc[self.m].values) or any(
                    self.out_data[self.out_data.columns[self.m]].values):
                out = np.arange(self.out_data.values.shape[0])[
                    self.out_data.values[self.m, :]==1]
                for o in out:
                    xycoord_i = self.canvas.coords(
                        self.connections[self.m][o].split('-')[0])
                    xycoord_o = self.canvas.coords(
                        self.connections[self.m][o].split('-')[1])
                    self.canvas.coords(self.connections[self.m][o], 
                            (xycoord_i[0] + self.cr, 
                             xycoord_i[1] + self.cr, 
                             xycoord_o[0] + self.cr, 
                             xycoord_o[1] + self.cr))
                inp = np.arange(self.out_data.values.shape[0])[
                    self.out_data.values[:, self.m]==1]
                for i in inp:
                    xycoord_i = self.canvas.coords(
                        self.connections[i][self.m].split('-')[0])
                    xycoord_o = self.canvas.coords(
                        self.connections[i][self.m].split('-')[1])
                    self.canvas.coords(self.connections[i][self.m], 
                            (xycoord_i[0] + self.cr, 
                             xycoord_i[1] + self.cr, 
                             xycoord_o[0] + self.cr, 
                             xycoord_o[1] + self.cr))
            # Update module location
            self.canvas.startxy[self.m] = (event.x, event.y)
    
    def module_out(self, name):
        """ Updates the output DataFrame.
        
        :param name: name of the model
        :type name: str
        """
        name_list = list(self.out_data.columns)
        m_num = [n.split('-')[1] for n in name_list if (
            len(n.split('-')) > 1) and (n.split('-')[0] == name)]
        name_list.append(name + '-' + str(len(m_num)))
        self.canvas.itemconfig('t'+str(self.modules), text = name_list[-1])
        values = self.out_data.values
        values = np.vstack((
                    np.hstack((values, np.zeros((values.shape[0],1)))),
                    np.zeros((1, values.shape[0]+1))))
        self.out_data = pd.DataFrame(values, 
                                     columns = name_list, 
                                     index = name_list)
        self.module_names.append(name_list[-1])

    def add_module(self, boxName):
        """ Creates a rectangular module with the corresponding text inside.
        
        :param boxName: name of the model
        :type boxName: str
        """
        text_w = self.controller.pages_font.measure(boxName+'-00') + 10
        self.canvas.create_rectangle(
            self.width/2 - text_w/2 , 
            self.height/2 - self.h/2, 
            self.width/2 + text_w/2, 
            self.height/2 + self.h/2, 
            tags = ('o'+str(self.modules), 'p'+str(self.modules)), 
            fill = self.bg, width = 3,
            activefill = '#dbaa21')
        self.canvas.create_text(
            self.width/2, 
            self.height/2, 
            font = self.controller.pages_font, 
            text = boxName, 
            tags = ('o'+str(self.modules), 't'+str(self.modules)), 
            fill = '#d0d4d9', 
            justify = tk.CENTER)
        self.canvas.tag_bind('t'+str(self.modules), 
                             "<Double-1>", self.OnDoubleClick)
        self.canvas.create_oval(
            self.width/2 - self.cr, 
            self.height/2 + self.h/2 - self.cr, 
            self.width/2 + self.cr, 
            self.height/2 + self.h/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'd'+str(self.modules)))
        self.canvas.tag_bind('d'+str(self.modules), 
                             "<Button-1>", self.join_modules)
        self.canvas.create_oval(
            self.width/2 - text_w/2 - self.cr, 
            self.height/2 - self.cr, 
            self.width/2 - text_w/2 + self.cr, 
            self.height/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'l'+str(self.modules)))
        self.canvas.tag_bind('l'+str(self.modules), 
                             "<Button-1>", self.join_modules)
        self.canvas.create_oval(
            self.width/2 - self.cr, 
            self.height/2 - self.h/2 - self.cr, 
            self.width/2 + self.cr, 
            self.height/2 - self.h/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'u'+str(self.modules)))
        self.canvas.tag_bind('u'+str(self.modules), 
                             "<Button-1>", self.join_modules)
        self.canvas.create_oval(
            self.width/2 + text_w/2 - self.cr, 
            self.height/2 - self.cr, 
            self.width/2 + text_w/2 + self.cr, 
            self.height/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'r'+str(self.modules)))
        self.canvas.tag_bind('r'+str(self.modules), 
                             "<Button-1>", self.join_modules)
        self.canvas.startxy.append((self.width/2, 
                                    self.height/2))
        self.connections[self.modules] = {}
        self.module_out(boxName)
        self.module_list.append(boxName)
        self.modules += 1
        self.saved = False
    
    def on_return_rename(self, event):
        """ This function renames a module to the input specified through 
        an entry widget. It then updates the corresponding rows and columns in
        the stored data."""
        
        moduleName = self.entry.get()
        if (moduleName in list(self.module_names)) and not(
                moduleName == list(self.module_names)[self.m]):
            messagebox.showwarning("Error", "This module already exists.")
        else:
            self.canvas.itemconfig('t'+str(self.m), text = moduleName)
            x0, y0, x1, y1 = self.canvas.coords('p'+str(self.m))
            text_w = self.controller.pages_font.measure(moduleName) + 20
            shift = (text_w-x1+x0)/2
            self.canvas.coords('p'+str(self.m), # Resize rectangle
                               x0 - shift, 
                               y0, 
                               x1 + shift, 
                               y1)
            x0, y0, x1, y1 = self.canvas.coords('l'+str(self.m))
            self.canvas.coords('l'+str(self.m), # Move left circle
                                x0 - shift, 
                                y0, 
                                x1 - shift, 
                                y1)
            x0, y0, x1, y1 = self.canvas.coords('r'+str(self.m))
            self.canvas.coords('r'+str(self.m), # Move left circle
                                x0 + shift, 
                                y0, 
                                x1 + shift, 
                                y1)
            self.entry.destroy()
            self.module_names[self.m] = moduleName
            
    def on_return_editLoop(self, event):
        """ This function renames loop conditions and updates the loop
        information."""
        
        newText = self.entry.get()
        conditions = self.canvas.itemcget(
                        self.selected[0], 'tags').split(' ')[1].split('-')
        self.canvas.itemconfig(self.selected[0], text = newText)
        self.entry.destroy()
        self.loops[int(conditions[1])][conditions[0]] = newText
        
    def OnDoubleClick(self, event):
        
        """ Executed when text is double clicked.
        Opens an entry box to edit the module name and updates the display and
        the stored data. """
        
        self.selected = self.canvas.find_overlapping(
            event.x-5, event.y-5, event.x+5, event.y+5)
        
        # If not loop text
        if len(self.canvas.itemcget(
                self.selected[0], 'tags').split(' ')[-2].split('-')) < 2:
            
            x0, y0, x1, y1 = self.canvas.coords(self.canvas.gettags("current")[0])
            if hasattr(self, 'entry'):
                self.entry.destroy()
            
            entryText = self.canvas.itemcget('t'+str(self.m), 'text')
            
            self.entry = tk.Entry(self.canvas, justify='center', 
                                  font = self.controller.pages_font)
    
            self.entry.insert(
                0, entryText)
            self.entry['selectbackground'] = '#d0d4d9'
            self.entry['exportselection'] = False
    
            self.entry.focus_force()
            self.entry.bind("<Return>", self.on_return_rename)
            self.entry.bind("<Escape>", lambda *ignore: self.entry.destroy())
            
            self.entry.place(x = x0, 
                              y = y0 + (y1-y0)/2, 
                              anchor = tk.W, width = x1 - x0)
        # If loop text
        else:
            x0, y0 = self.canvas.coords(self.selected[0])
            if hasattr(self, 'entry'):
                self.entry.destroy()

            # condition = self.canvas.itemcget(
            #             self.selected[0], 'tags').split(' ')[-2]#.split('-')[0]
            entryText = self.canvas.itemcget(self.selected[0], 'text')
            
            self.entry = tk.Entry(self.canvas, justify='center', 
                                  font = self.controller.pages_font)
            self.entry.insert(0, entryText)
            # self.entry1['selectbackground'] = '#d0d4d9'
            self.entry['exportselection'] = False
    
            self.entry.focus()
            self.entry.bind("<Return>", self.on_return_editLoop)
            self.entry.bind("<Escape>", lambda *ignore: self.entry.destroy())
            text_w = self.controller.pages_font.measure(entryText) + 20
            self.entry.place(x = x0 - text_w/2, 
                          y = y0, 
                          anchor = tk.W, 
                          width = text_w)
                
    def delete_sel(self):
        """ Deletes last selected module"""
        if self.canvas.selected:
            if self.isLoop:
                self.canvas.delete('loop-'+str(self.m))
                self.loops[self.m] = -1
            elif not(self.m == 0):
                self.canvas.delete('o'+str(self.m))
                
                col = self.out_data.columns[self.m]
                self.out_data[col] = 0
                self.out_data.loc[col] = 0
                self.saved = False
                
    def join_modules(self, event):
        """ Draws a connecting line between two connecting circles. """
        if self.draw:
            tags = self.canvas.gettags(self.canvas.find_overlapping(
            event.x-self.cr, event.y-self.cr, 
            event.x+self.cr, event.y+self.cr)[-1])
            tag2 = tags[-2] if tags[-1] == "current" else tags[-1]
            if tag2[0] in ['d', 'l', 'u', 'r'] and int(
                    tag2[1:]) != int(self.tag[1:]):
                self.canvas.create_line(
                            self.canvas.linestartxy[0] + self.cr, 
                            self.canvas.linestartxy[1] + self.cr, 
                            self.canvas.coords(tag2)[0] + self.cr, 
                            self.canvas.coords(tag2)[1] + self.cr,
                            fill = "red", 
                            arrow = tk.LAST, 
                            tags = ('o'+str(int(self.tag[1:])), 
                                  'o'+str(int(tag2[1:])), self.tag + '-' + tag2))
                self.out_data.iloc[int(self.tag[1:])][int(tag2[1:])] = 1
                self.connections[
                    int(self.tag[1:])][int(tag2[1:])] = self.tag + '-' + tag2
            self.draw = False
            self.saved = False
        else:
            tags = self.canvas.gettags(self.canvas.find_overlapping(
            event.x-self.cr, event.y-self.cr, 
            event.x+self.cr, event.y+self.cr)[-1])
            self.tag = tags[-2] if tags[-1] == "current" else tags[-1]
            self.canvas.linestartxy = self.canvas.coords(self.tag)#(event.x, event.y)
            self.draw = True

    def save_file_as(self):
        
        self.save_path = asksaveasfile(mode='w')
        self.save_file()
        
    def save_file(self):
        
        if self.save_path == '':
            self.save_path = asksaveasfile(defaultextension = '.xml', filetypes = 
                                      [('XML file', '.xml'), 
                                       ('All Files', '*.*')])
        if self.save_path is not None: # asksaveasfile return `None` if dialog closed with "cancel".
            # Transform input for output file
            data = self.out_data.copy()
            if np.sum(data.values[0,:]) == 0:
                messagebox.showwarning(
                    "Error", "Initialiser is not connected to any module.")
            elif np.sum(data.values[:,1]) == 0:
                messagebox.showwarning(
                    "Error", "Output is not connected to any module.")
            idx = (np.sum(data.values, axis = 0) 
                   + np.sum(data.values, axis = 1)) < 1
            col = np.array(data.columns)
            for c in np.arange(len(idx))[idx]:
                data = data.drop(columns=col[c], index=col[c])
                
            print(col)
            print(self.module_names)
            loop_modules = np.unique([v for a in self.loops for v in a['mod']])
            out_loops = np.zeros_like(self.loops)
            
            values = data.values.astype(bool)
            mn = np.array(self.module_names)
            
            s = Settings()
            s.new_config_file(self.save_path.name)
            s.parse_XML()
            s.filename = self.save_path.name
            s.append_pipeline_module(self.module_list[0], # Initialiser
                                  mn[0],
                                  "",
                                  {},
                                  list(mn[values[:,0]]),
                                  list(mn[values[0,:]]),
                                  None,
                                  self.canvas.startxy[0])
            for i in np.arange(len(mn)-2)+2:
                xml_parent = None
                parent_loops = []
                if mn[i] in loop_modules: # Model in any loop
                    for x, loop in enumerate(self.loops):
                        if mn[i] in loop['mod']: # Model in this loop
                            if not out_loops[x]: # Loop already defined
                                s.append_pipeline_loop(self.loops[x]['type'],
                                            self.loops[x]['condition'],
                                            "loop"+str(x),
                                            parent_loops,
                                            list(loop['mod']),
                                            xml_parent,
                                            self.loops[x]['coord']
                                            )
                                out_loops[x] = 1
                            xml_parent = "loop"+str(x) # parent is the last loop
                            parent_loops.append("loop"+str(x))
                
                s.append_pipeline_module(self.module_list[i],
                  mn[i],
                  "",
                  {},
                  list(mn[values[:,i]]),
                  list(mn[values[i,:]]),
                  xml_parent,
                  self.canvas.startxy[i])
                
            s.append_pipeline_module(self.module_list[1], # Out
                      mn[1],
                      "",
                      {},
                      list(mn[values[:,1]]),
                      list(mn[values[1,:]]),
                      None,
                      self.canvas.startxy[1])
            s.write_to_XML()
            self.saved = True
         
    def upload(self):
        
        self.reset()
        filename = askopenfilename(initialdir = os.getcwd(), 
                                   title = 'Select a file', 
                                   defaultextension = '.xml', 
                                   filetypes = [('XML file', '.xml'), 
                                                ('All Files', '*.*')])
        if filename is not None:
            data = open(filename,'r')

            # for n, point in enumerate(data):
    
    def reset(self):
        
        msg = messagebox.askyesnocancel(
            'Info', 'Are you sure you want to reset the canvas?')
        if msg:
            self.canvas.delete(tk.ALL) # Reset canvas
            
            if hasattr(self, 'entry'):
                self.entry.destroy()
            if hasattr(self, 'entry1'):
                self.entry1.destroy()
            if hasattr(self, 'entry2'):
                self.entry2.destroy()
            
            self.out_data = pd.DataFrame(np.zeros((2,2)), 
                                         columns = ['Initialiser', 'Output'], 
                                         index = ['Initialiser', 'Output'])
            x0 = self.width/2 - (
            self.controller.pages_font.measure('Initialiser')+10)/2
            y0 = self.h
            self.canvas.create_rectangle(x0, y0, x0 + self.w, y0 + self.h, 
                                     tags = 'p0', fill = self.bg, width = 3,
                                     activefill = '#dbaa21')
            self.canvas.create_text(x0 + self.w/2, y0 + self.h/2, 
                                    text = 'Initialiser', tags = 't0', 
                                    fill = '#d0d4d9', 
                                    font = self.controller.pages_font)
            self.canvas.create_oval(
                            x0 + self.w/2-self.cr, y0 + self.h-self.cr, 
                            x0 + self.w/2+self.cr, y0 + self.h+self.cr, 
                            width=2, fill = 'black', tags='d0')
            self.canvas.tag_bind('d0', "<Button-1>", self.join_modules)
            # Output module
            h_out = self.height - 2*self.h
            self.canvas.create_rectangle(x0, h_out, x0 + self.w, h_out + self.h, 
                                         tags = ('p1'), 
                                         fill = self.bg, width = 3,
                                         activefill = '#dbaa21')
            self.canvas.create_text(x0 + self.w/2, h_out + self.h/2, 
                                    text = 'Output', tags = ('t1'), 
                                    fill = '#d0d4d9', 
                                    font = self.controller.pages_font)
            self.canvas.create_oval(
                            x0 + self.w/2 - self.cr, 
                            h_out - self.cr, 
                            x0 + self.w/2 + self.cr, 
                            h_out  + self.cr,
                            width=2, fill = 'black', tags = ('u1'))
            self.canvas.tag_bind('u1', "<Button-1>", self.join_modules)
            
            self.draw = False
            self.canvas.startxy = []
            self.canvas.startxy.append((x0 + self.w/2, 
                                        y0 + self.h/2))
            self.canvas.startxy.append((x0 + self.w/2, 
                                        h_out + self.h/2))
            self.connections = {}
            self.connections[0] = {}
            self.connections[1] = {}
            self.module_list = ['Initialiser', 'Output']
            self.module_names = ['Initialiser', 'Output']
            self.loops = []
            self.drawLoop = False
            self.modules = 2
            self.l = 0
            self.saved = False
    
if __name__ == "__main__":
    app = aidCanvas()
    app.mainloop()