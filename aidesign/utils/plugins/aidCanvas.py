# Import the required libraries
import tkinter as tk
from tkinter import font  as tkfont # python 3
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd

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
        
        self.out_data = pd.DataFrame(np.zeros((1,1)), 
                                     columns = ['Initialisation'], 
                                     index = ['Initialisation'])
        self.connections = {}
        self.connections[0] = {}
        # Create plugin
        self.w, self.h = 100, 50
        x0 = self.width/2 - (
            self.controller.pages_font.measure('Initialisation')+10)/2
        y0 = 50
        self.cr = 4
        
        self.canvas.create_rectangle(x0, y0, x0 + self.w, y0 + self.h, 
                                     tags = 'p0', fill = self.bg, width = 3,
                                     activefill = '#dbaa21')
        self.canvas.create_text(x0 + self.w/2, y0 + self.h/2, 
                                text = 'Initialisation', tags = 't0', 
                                fill = '#d0d4d9', 
                                font = self.controller.pages_font)
        self.canvas.create_oval(
                        x0 + self.w/2-self.cr, y0 + self.h-self.cr, 
                        x0 + self.w/2+self.cr, y0 + self.h+self.cr, 
                        width=2, fill = 'black', tags='d0')
        self.canvas.tag_bind('d0', "<Button-1>", self.join_plugins)
        self.draw = False
        self.canvas.startxy.append((x0 + self.w/2, 
                                    y0 + self.h/2))
        
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind('<Button-1>', self.select)
        
        # modules = ['Data preprocessing', 'Modelling', 'Decision making', 'User Feedback Adaptation']
        
        self.modules = 1
        # for m, module in enumerate(modules):
        tk.Button(
            self, text = 'Data preprocessing', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_plugin('Data preprocessing')).grid(column = 5, row = 1)
        tk.Button(
            self, text = 'Modelling', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_plugin('Modelling')).grid(column = 5, row = 2)
        tk.Button(
            self, text = 'Decision making', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_plugin('Decision making')).grid(column = 5, row = 3)
        tk.Button(
            self, text = 'User Feedback Adaptation', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_plugin('User Feedback Adaptation')).grid(column = 5, row = 4)
                
        tk.Button(
            self, text = 'Delete selection', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = self.delete_sel).grid(column = 5, row = 5)

    def select(self, event):
        """ Selects the plugin at the mouse location """
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
            
        self.m = int(self.canvas.gettags("current")[0][1:])
        
    def on_drag(self, event):
        """ Uses the mouse location to move the plugin and its text."""
        
        self.select(event)
        
        self.m = int(self.canvas.gettags("current")[0][1:])
        dx = event.x - self.canvas.startxy[self.m][0]
        dy = event.y - self.canvas.startxy[self.m][1]
        
        self.canvas.move('o'+str(self.m), dx, dy) #Plugin
        
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
        self.canvas.startxy[self.m] = (event.x, event.y)
    
    def plugin_out(self, name):
        name_list = list(self.out_data.columns)
        m_num = [n.split('-')[1] for n in name_list if n.split('-')[0]==name]
        name_list.append(name + '-' + str(len(m_num)))
        values = self.out_data.values
        values = np.vstack((
                    np.hstack((values, np.zeros((values.shape[0],1)))),
                    np.zeros((1, values.shape[0]+1))))
        self.out_data = pd.DataFrame(values, 
                                     columns = name_list, 
                                     index = name_list)
    
    def add_plugin(self, boxName):
        """ Creates a plugin rectangle with the corresponding text inside."""
        text_w = self.controller.pages_font.measure(boxName)+10
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
        self.canvas.create_oval(
            self.width/2 - self.cr, 
            self.height/2 + self.h/2 - self.cr, 
            self.width/2 + self.cr, 
            self.height/2 + self.h/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'd'+str(self.modules)))
        self.canvas.tag_bind('d'+str(self.modules), 
                             "<Button-1>", self.join_plugins)
        self.canvas.create_oval(
            self.width/2 - text_w/2 - self.cr, 
            self.height/2 - self.cr, 
            self.width/2 - text_w/2 + self.cr, 
            self.height/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'l'+str(self.modules)))
        self.canvas.tag_bind('l'+str(self.modules), 
                             "<Button-1>", self.join_plugins)
        self.canvas.create_oval(
            self.width/2 - self.cr, 
            self.height/2 - self.h/2 - self.cr, 
            self.width/2 + self.cr, 
            self.height/2 - self.h/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'u'+str(self.modules)))
        self.canvas.tag_bind('u'+str(self.modules), 
                             "<Button-1>", self.join_plugins)
        self.canvas.create_oval(
            self.width/2 + text_w/2 - self.cr, 
            self.height/2 - self.cr, 
            self.width/2 + text_w/2 + self.cr, 
            self.height/2 + self.cr, 
            width = 2, 
            fill = 'black', 
            tags = ('o'+str(self.modules), 'r'+str(self.modules)))
        self.canvas.tag_bind('r'+str(self.modules), 
                             "<Button-1>", self.join_plugins)
        self.canvas.startxy.append((self.width/2, 
                                    self.height/2))
        self.connections[self.modules] = {}
        self.modules += 1
        self.plugin_out(boxName)

    def delete_sel(self):
        """ Deletes last selected plugin"""
        if self.canvas.selected and not(self.m == 0):
            self.canvas.delete('o'+str(self.m))
            
            col = self.out_data.columns[self.m]
            self.out_data[col] = 0
            self.out_data.loc[col] = 0
                
    def join_plugins(self, event):
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
        else:
            tags = self.canvas.gettags(self.canvas.find_overlapping(
            event.x-self.cr, event.y-self.cr, 
            event.x+self.cr, event.y+self.cr)[-1])
            self.tag = tags[-2] if tags[-1] == "current" else tags[-1]
            self.canvas.linestartxy = self.canvas.coords(self.tag)#(event.x, event.y)
            self.draw = True

# AI Design
# XML design
if __name__ == "__main__":
    app = aidCanvas()
    app.mainloop()