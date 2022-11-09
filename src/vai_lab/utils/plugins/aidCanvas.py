from vai_lab.Data.xml_handler import XML_handler
from vai_lab._types import DictT

import os
import numpy as np
import pandas as pd
from typing import List, Literal,Tuple

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
from vai_lab._import_helper import get_lib_parent_dir


_PLUGIN_READABLE_NAMES = {"aid_canvas": "default",
                          "aidCanvas": "alias",
                          "aid": "alias",
                          "AID": "alias"}               # type:ignore
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                          "required_children": None}    # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                          # type:ignore


class aidCanvas(tk.Frame):
    """Canvas for graphical specification of pipeline modules"""

    def __init__(self, parent, controller, config: dict):
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."

        super().__init__(parent, bg=parent['bg'])
        self.bg = parent['bg']
        self.controller = controller

        script_dir = get_lib_parent_dir()
        self.tk.call('wm', 'iconphoto', self.controller._w, ImageTk.PhotoImage(
            file=os.path.join(os.path.join(
                script_dir,
                'utils',
                'resources',
                'Assets',
                'VAILabsIcon.ico'))))
        self.my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(
            script_dir,
            'utils',
            'resources',
            'Assets',
            'VAILabs.png')).resize((200, 200)))

        # self.grid_rowconfigure(tuple(range(2)), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(self, bg=self.bg)
        frame2 = tk.Frame(self, bg=self.bg)
        frame3 = tk.Frame(self, bg=self.bg)
        frame4 = tk.Frame(self, bg=self.bg)

        self.my_label = tk.Label(frame2, image=self.my_img1, bg=parent['bg'], anchor = 'center')
        self.my_label.grid(column=5, row=0, padx=(10, 10), pady=(10, 10), sticky="nwse")

        # Create canvas
        self.width, self.height = 700, 700
        self.canvas = tk.Canvas(frame1, width=self.width,
                                height=self.height, background="white")
        # self.canvas = ResizingCanvas(frame1, width=self.width,
        #     height=self.height, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

        self.canvas_startxy: List[Tuple] = []
        self.out_data = pd.DataFrame()
        self.connections: DictT = {}
        self.modules = 0
        self.module_list: List[str] = []
        self.module_names: List[str] = []

        # Create module
        self.w, self.h = 100, 50
        self.cr = 4

        # Initialiser module
        self.add_module('Initialiser', self.width/2, self.h, ini=True)
        self.add_module('Output', self.width/2, self.height - self.h, out=True)

        self.draw = False
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind('<Button-1>', self.select)
        self.l = 0  # number of loops
        self.drawLoop = False
        self.loops: List[DictT] = []

        # self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # for m, module in enumerate(modules):
        tk.Button(
            frame4, text='Data processing', fg='white', bg=parent['bg'],
            height=3, width=25, font=self.controller.pages_font,
            command=lambda: self.add_module('Data Processing',
                                            self.width/2,
                                            self.height/2)
        ).grid(column=5, row=1, padx=(10, 10), sticky="news")
        tk.Button(
            frame4, text='Modelling', fg='white', bg=parent['bg'],
            height=3, width=25, font=self.controller.pages_font,
            command=lambda: self.add_module('Modelling',
                                            self.width/2,
                                            self.height/2)
        ).grid(column=5, row=2, padx=(10, 10), sticky="news")
        tk.Button(
            frame4, text='Decision making', fg='white', bg=parent['bg'],
            height=3, width=25, font=self.controller.pages_font,
            command=lambda: self.add_module('Decision Making',
                                            self.width/2,
                                            self.height/2)
        ).grid(column=5, row=3, padx=(10, 10), sticky="news")
        tk.Button(
            frame4, text='User Interaction', fg='white', bg=parent['bg'],
            height=3, width=25, font=self.controller.pages_font,
            command=lambda: self.add_module('User Interaction',
                                            self.width/2,
                                            self.height/2)
        ).grid(column=5, row=4, padx=(10, 10), sticky="news")
        tk.Button(
            frame4, text = 'Input data', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_module('Input Data', 
                                              self.width/2, 
                                              self.height/2)
            ).grid(column = 5, row = 5, padx=(0,10), sticky="news")        
        tk.Button(
            frame4, text = 'Data Storage', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = lambda: self.add_module('Data Storage', 
                                              self.width/2, 
                                              self.height/2)
            ).grid(column = 5, row = 6, padx=(0,10), sticky="news")
        tk.Button(
            frame4, text = 'Delete selection', fg = 'white', bg = parent['bg'],
            height = 3, width = 25, font = self.controller.pages_font,
            command = self.delete_sel).grid(column = 5, row = 7, sticky="news"
                                            , padx=(0,10), pady=(0,10))
        
        tk.Button(
            frame3, text='Upload', fg='white', bg=parent['bg'],
            height=3, width=15, font=self.controller.pages_font,
            command=self.upload).grid(column=0, row=10, sticky="news",
                                      padx=(10, 0), pady=(0, 10))
        tk.Button(
            frame3, text='Save', fg='white', bg=parent['bg'],
            height=3, width=15, font=self.controller.pages_font,
            command=self.save_file).grid(column=1, row=10, sticky="news", pady=(0, 10))
        tk.Button(
            frame3, text='Reset', fg='white', bg=parent['bg'],
            height=3, width=15, font=self.controller.pages_font,
            command=self.reset).grid(column=2, row=10, sticky="news", pady=(0, 10))
        tk.Button(
            frame3, text='Done', fg='white', bg=parent['bg'],
            height=3, width=15, font=self.controller.pages_font,
            command=self.check_quit).grid(column=3, row=10, sticky="news", pady=(0, 10))

        self.save_path = ''
        self.saved = True

        frame1.grid(column=0, row=0, rowspan=2, sticky="nsew")
        frame2.grid(column=1, row=0, sticky="nwse")
        frame3.grid(column=0, row=2, sticky="swe")
        frame4.grid(column=1, row=1, sticky="nse")
        
        frame3.grid_columnconfigure(4, weight=1)
        frame4.grid_rowconfigure(7, weight=1)

    def class_list(self, value):
        """ Temporary fix """
        return value

    def on_return_display(self, event):
        """ Defines the type of loop and condition for the indicated loop
        """
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
            font=self.controller.pages_font,
            text=condition,
            tags=('loop-'+str(self.l-1), key+'-'+str(self.l-1)),
            justify=tk.CENTER)
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
                    aux = self.canvas.itemcget(mod, 'tags').split(' ')
                    if aux[0][:4] != 'loop':
                        if len(aux) == 2 and len(aux[1]) > 1 and aux[1][0] == 't':
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
                self.entry1.bind(
                    "<Escape>", lambda *ignore: self.entry1.destroy())

                self.entry1.place(
                    x=self.start_x + 10,
                    y=self.start_y + 20,
                    anchor=tk.W,
                    width=self.controller.pages_font.measure(text)+10)
                text = 'Condition'
                self.entry2 = tk.Entry(self.canvas, justify='center',
                                       font=self.controller.pages_font)
                self.entry2.insert(0, text)
                self.entry2['exportselection'] = False

                self.entry2.bind("<Return>", self.on_return_display)
                self.entry2.bind(
                    "<Escape>", lambda *ignore: self.entry.destroy())

                self.entry2.place(
                    x=self.curX-self.controller.pages_font.measure(text)-20,
                    y=self.start_y + 20,
                    anchor=tk.W,
                    width=self.controller.pages_font.measure(text)+10)

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
                aux = self.canvas.itemcget(mod, 'tags').split(' ')[-1]
                if len(aux) == 2 and aux[0] == 't':
                    self.loops[l]['mod'].append(self.canvas.itemcget(
                        mod, 'text'))
        # print('Updated loop info:', self.loops)
        
    def select(self, event):
        """ Selects the module at the mouse location. """
        self.selected = self.canvas.find_overlapping(
            event.x-5, event.y-5, event.x+5, event.y+5)
        if self.selected:
            if len(self.selected) > 2:
                self.canvas.selected = self.selected[-2]
            else:
                self.canvas.selected = self.selected[-1]
            # self.canvas_startxy = (event.x, event.y)
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
                                                         outline='#4ff07a',
                                                         tag='loop-'+str(self.l))
                # ,fill = '#b3ffc7')
                self.drawLoop = True
                if self.l == 0:
                    self.canvas.tag_lower('loop-'+str(self.l))
                else:
                    self.canvas.tag_raise(
                        'loop-'+str(self.l), 'loop-'+str(self.l-1))

        if len(self.canvas.gettags("current")) > 0:
            if any('loop' in value for value in self.canvas.gettags("current")):
                self.isLoop = True
                self.m = [int(el.split('-')[-1]) for el in self.canvas.gettags("current") if 'loop' in el][0]
            else:
                self.isLoop = False
                self.canvas.gettags("current")
                #Preference to objects with text
                if any(el[0] == 't' for el in self.canvas.gettags("current")):
                    self.m = [int(el[1:]) for el in self.canvas.gettags("current") if el[0] == 't'][0]
                else:
                    self.m = [int(el[1:]) for el in self.canvas.gettags("current") if el[1:].isdigit()][0]

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
            sel_obj = [int(el[1:]) for el in self.canvas.gettags("current") if el[0] == 't']
            if len(sel_obj) > 0:
                self.m = sel_obj[0]
                
                dx = event.x - self.canvas_startxy[self.m][0]
                dy = event.y - self.canvas_startxy[self.m][1]
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
                            self.connections[o][self.m].split('-')[0])
                        xycoord_o = self.canvas.coords(
                            self.connections[o][self.m].split('-')[1])
                        self.canvas.coords(self.connections[o][self.m], 
                                (xycoord_i[0] + self.cr, 
                                 xycoord_i[1] + self.cr, 
                                 xycoord_o[0] + self.cr, 
                                 xycoord_o[1] + self.cr))
                    inp = np.arange(self.out_data.values.shape[0])[
                        self.out_data.values[:, self.m]==1]
                    for i in inp:
                        xycoord_i = self.canvas.coords(
                            self.connections[self.m][i].split('-')[0])
                        xycoord_o = self.canvas.coords(
                            self.connections[self.m][i].split('-')[1])
                        self.canvas.coords(self.connections[self.m][i], 
                                (xycoord_i[0] + self.cr, 
                                 xycoord_i[1] + self.cr, 
                                 xycoord_o[0] + self.cr, 
                                 xycoord_o[1] + self.cr))
                # Update module location
                self.canvas_startxy[self.m] = (event.x, event.y)
    
    def module_out(self, name, iid):
        """ Updates the output DataFrame.

        :param name: name of the model
        :type name: str
        """
        name_list = list(self.out_data.columns)
        m_num = [n for n in name_list if (n.split('-')[0] == name)]
        if len(m_num) > 0:
            name_list.append(name + '-' + str(len(m_num)))
        else:
            name_list.append(name)
        self.canvas.itemconfig('t'+str(iid), text = name_list[-1])
        values = self.out_data.values
        values = np.vstack((
            np.hstack((values, np.zeros((values.shape[0], 1)))),
            np.zeros((1, values.shape[0]+1))))
        self.out_data = pd.DataFrame(values,
                                     columns=name_list,
                                     index=name_list)
        self.module_names.append(name_list[-1])

    def add_module(self, boxName, x, y, ini = False, out = False, iid = None):
        """ Creates a rectangular module with the corresponding text inside.

        :param boxName: name of the model
        :type boxName: str
        """
        iid = self.modules if iid is None else iid
        if not ini and not out:
            tag = ('o'+str(iid),)
        else: #Make initialisation and output unmoveable
            tag = ('n0',)
        text_w = self.controller.pages_font.measure(boxName+'-00') + 10
        self.canvas.create_rectangle(
            x - text_w/2 , 
            y - self.h/2, 
            x + text_w/2, 
            y + self.h/2, 
            tags = tag + ('p'+str(iid),), 
            fill = self.bg, width = 3,
            activefill = '#dbaa21')
        self.canvas.create_text(
            x, 
            y, 
            font = self.controller.pages_font, 
            text = boxName, 
            tags = tag + ('t'+str(iid),), 
            fill = '#d0d4d9', 
            justify = tk.CENTER)
        self.canvas.tag_bind('t'+str(iid), 
                             "<Double-1>", self.OnDoubleClick)
        if not out:
            self.canvas.create_oval(
                x - self.cr, 
                y + self.h/2 - self.cr, 
                x + self.cr, 
                y + self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('d'+str(iid),))
            self.canvas.tag_bind('d'+str(iid), 
                                 "<Button-1>", self.join_modules)

        if not ini:
            self.canvas.create_oval(
                x - self.cr, 
                y - self.h/2 - self.cr, 
                x + self.cr, 
                y - self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('u'+str(iid),))
            self.canvas.tag_bind('u'+str(iid), 
                                 "<Button-1>", self.join_modules)

        if not out and not ini:
            self.canvas.create_oval(
                x - text_w/2 - self.cr, 
                y - self.cr, 
                x - text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('l'+str(iid),))
            self.canvas.tag_bind('l'+str(iid), 
                                 "<Button-1>", self.join_modules)

            self.canvas.create_oval(
                x + text_w/2 - self.cr, 
                y - self.cr, 
                x + text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('r'+str(iid),))
            self.canvas.tag_bind('r'+str(iid), 
                                 "<Button-1>", self.join_modules)
        self.canvas_startxy.append((x,
                                    y))
        self.connections[iid] = {}
        self.module_out(boxName, iid)
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
            self.canvas.itemconfig('t'+str(self.m), text=moduleName)
            x0, y0, x1, y1 = self.canvas.coords('p'+str(self.m))
            text_w = self.controller.pages_font.measure(moduleName) + 20
            shift = (text_w-x1+x0)/2
            self.canvas.coords('p'+str(self.m),  # Resize rectangle
                               x0 - shift,
                               y0,
                               x1 + shift,
                               y1)
            x0, y0, x1, y1 = self.canvas.coords('l'+str(self.m))
            self.canvas.coords('l'+str(self.m),  # Move left circle
                               x0 - shift,
                               y0,
                               x1 - shift,
                               y1)
            x0, y0, x1, y1 = self.canvas.coords('r'+str(self.m))
            self.canvas.coords('r'+str(self.m),  # Move left circle
                               x0 + shift,
                               y0,
                               x1 + shift,
                               y1)
            self.entry.destroy()
            self.module_names[self.m] = moduleName
            self.saved = False

    def on_return_editLoop(self, event):
        """ This function renames loop conditions and updates the loop
        information."""

        newText = self.entry.get()
        conditions = self.canvas.itemcget(
            self.selected[0], 'tags').split(' ')[1].split('-')
        self.canvas.itemconfig(self.selected[0], text=newText)
        self.entry.destroy()
        self.loops[int(conditions[1])][conditions[0]] = newText
        self.saved = False

    def OnDoubleClick(self, event):
        """ Executed when text is double clicked.
        Opens an entry box to edit the module name and updates the display and
        the stored data. """

        self.selected = self.canvas.find_overlapping(
            event.x-5, event.y-5, event.x+5, event.y+5)

        # If not loop text
        if len(self.canvas.itemcget(
                self.selected[0], 'tags').split(' ')[-2].split('-')) < 2:

            x0, y0, x1, y1 = self.canvas.coords(
                self.canvas.gettags("current")[0])
            if hasattr(self, 'entry'):
                self.entry.destroy()

            entryText = self.canvas.itemcget('t'+str(self.m), 'text')

            self.entry = tk.Entry(self.canvas, justify='center',
                                  font=self.controller.pages_font)

            self.entry.insert(
                0, entryText)
            self.entry['selectbackground'] = '#d0d4d9'
            self.entry['exportselection'] = False

            self.entry.focus_force()
            self.entry.bind("<Return>", self.on_return_rename)
            self.entry.bind("<Escape>", lambda *ignore: self.entry.destroy())

            self.entry.place(x=x0,
                             y=y0 + (y1-y0)/2,
                             anchor=tk.W, width=x1 - x0)
        # If loop text
        else:
            x0, y0 = self.canvas.coords(self.selected[0])
            if hasattr(self, 'entry'):
                self.entry.destroy()

            # condition = self.canvas.itemcget(
            #             self.selected[0], 'tags').split(' ')[-2]#.split('-')[0]
            entryText = self.canvas.itemcget(self.selected[0], 'text')

            self.entry = tk.Entry(self.canvas, justify='center',
                                  font=self.controller.pages_font)
            self.entry.insert(0, entryText)
            # self.entry1['selectbackground'] = '#d0d4d9'
            self.entry['exportselection'] = False
            
            self.entry.focus()
            self.entry.bind("<Return>", self.on_return_editLoop)
            self.entry.bind("<Escape>", lambda *ignore: self.entry.destroy())
            text_w = self.controller.pages_font.measure(entryText) + 20
            self.entry.place(x=x0 - text_w/2,
                             y=y0,
                             anchor=tk.W,
                             width=text_w)

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
                self.module_names[self.m] = None

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
                            fill = "red",  width = 2,
                            arrow = tk.LAST, arrowshape = (12,10,5), 
                            tags = ('o'+str(int(self.tag[1:])), 
                                  'o'+str(int(tag2[1:])), self.tag + '-' + tag2))
                self.out_data.iloc[int(self.tag[1:])][int(tag2[1:])] = 1
                self.connections[int(tag2[1:])][
                    int(self.tag[1:])] = self.tag + '-' + tag2
            self.draw = False
            self.saved = False
        else:
            tags = self.canvas.gettags(self.canvas.find_overlapping(
                event.x-self.cr, event.y-self.cr,
                event.x+self.cr, event.y+self.cr)[-1])
            self.tag = tags[-2] if tags[-1] == "current" else tags[-1]
            self.canvas.linestartxy = self.canvas.coords(
                self.tag)  # (event.x, event.y)
            self.draw = True

    def save_file_as(self):

        self.save_path = asksaveasfile(mode='w')
        self.save_file()

    def save_file(self):

        if self.save_path == '':
            self.save_path = asksaveasfile(defaultextension='.xml', filetypes=[('XML file', '.xml'),
                                                                               ('All Files', '*.*')])
        # asksaveasfile return `None` if dialog closed with "cancel".
        if self.save_path is not None:
            # Transform input for output file
            data = self.out_data.copy()
            if np.sum(data.values[0, :]) == 0:
                messagebox.showwarning(
                    "Error", "Initialiser is not connected to any module.")
            elif np.sum(data.values[:, 1]) == 0:
                messagebox.showwarning(
                    "Error", "Output is not connected to any module.")
            idx = (np.sum(data.values, axis=0)
                   + np.sum(data.values, axis=1)) < 1
            col = np.array(data.columns)
            for c in np.arange(len(idx))[idx]:
                data = data.drop(columns=col[c], index=col[c])

            loop_modules = np.unique([v for a in self.loops for v in a['mod']])
            out_loops = np.zeros_like(self.loops)

            values = data.values.astype(bool)
            mn = np.array(self.module_names)
            mn_id = [m is not None for m in mn]
            mn = mn[mn_id]

            # to avoid numpy bug during elementwise comparison of lists 
            loop_modules.dtype = mn.dtype if len(loop_modules) == 0 else loop_modules.dtype
            
            self.controller.s.update_module_coords(self.module_list[0],[self.canvas_startxy[0], 0, self.connections[0]])
            self.controller.s.append_module_relationships(self.module_list[0],list(mn[values[:,0]]),list(mn[values[0,:]]))
            self.controller.s.filename = self.save_path.name
            for i, mnn in enumerate(mn_id):
                if (i > 1) and mnn:
                    xml_parent = None
                    parent_loops = []
                    if mn[i] in loop_modules:  # Model in any loop
                        for x, loop in enumerate(self.loops):
                            if mn[i] in loop['mod']:  # Model in this loop
                                if not out_loops[x]:  # Loop already defined
                                    self.controller.s.append_pipeline_loop(self.loops[x]['type'],
                                                                           self.loops[x]['condition'],
                                                                           "loop" +
                                                                           str(x),
                                                                           parent_loops,
                                                                           list(
                                                                               loop['mod']),
                                                                           xml_parent,
                                                                           self.loops[x]['coord']
                                                                           )
                                    out_loops[x] = 1
                                # parent is the last loop
                                xml_parent = "loop"+str(x)
                                parent_loops.append("loop"+str(x))

                    self.controller.s.append_pipeline_module(self.module_list[i],
                                                             mn[i],
                                                             "",
                                                             {},
                                                             list(
                                                                 mn[values[:, i]]),
                                                             list(
                                                                 mn[values[i, :]]),
                                                             xml_parent,
                                                             [self.canvas_startxy[i], i, self.connections[i]])

            self.controller.s.append_pipeline_module(self.module_list[1],  # Out
                                                     mn[1],
                                                     "",
                                                     {},
                                                     list(mn[values[:, 1]]),
                                                     list(mn[values[1, :]]),
                                                     None,
                                                     [self.canvas_startxy[1], 1, self.connections[1]])
            self.controller.s.write_to_XML()
            self.saved = True
            self.controller._append_to_output(
                "xml_filename", self.save_path.name)

    def upload(self):

        filename = askopenfilename(initialdir=os.getcwd(),
                                   title='Select a file',
                                   defaultextension='.xml',
                                   filetypes=[('XML file', '.xml'),
                                              ('All Files', '*.*')])
        if filename is not None and len(filename) > 0:
            self.reset()

            s = XML_handler()
            s.load_XML(filename)
            # s._print_pretty(s.loaded_modules)
            modules = s.loaded_modules
            modout = modules['Output']
            del modules['Initialiser'], modules['Output'] # They are generated when resetting
            disp_mod = ['Initialiser', 'Output']
            id_mod = [0, 1]

            # Place the modules
            id_mod, disp_mod = self.place_modules(modules, id_mod, disp_mod)
            self.draw_connection(modules, id_mod, disp_mod)
            connect = list(modout['coordinates'][2].keys())
            for p, parent in enumerate(modout['parents']):
                    parent_id = id_mod[np.where(np.array(disp_mod) == parent)[0][0]]
                    out, ins = modout['coordinates'][2][connect[p]].split('-')
                    xout, yout, _ , _ = self.canvas.coords(out[0]+str(parent_id))
                    xins, yins, _, _ =self.canvas.coords(ins[0]+str(1))
                    self.canvas.create_line(
                                xout + self.cr, 
                                yout + self.cr, 
                                xins + self.cr, 
                                yins + self.cr,
                                fill = "red",  width = 2,
                                arrow = tk.LAST, arrowshape = (12,10,5), 
                                tags = ('o'+str(parent_id), 
                                      'o'+str(1), modout['coordinates'][2][connect[p]]))
                    self.out_data.iloc[int(parent_id)][1] = 1
                    self.connections[1][
                        int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(1)
            self.controller._append_to_output("xml_filename",filename)

    def place_modules(self, modules, id_mod, disp_mod):
        """Places the modules in the dictionary in the canvas.
        :param modules: dict type of modules in the pipeline.
        """
        for key in [key for key, val in modules.items() if type(val) == dict]:
            if modules[key]['class'] == 'loop':
                self.l += 1
                # Extracts numbers from string
                l = int(
                    ''.join(map(str, list(filter(str.isdigit, modules[key]['name'])))))
                x0, y0, x1, y1 = modules[key]['coordinates']
                self.canvas.create_rectangle(x0, y0,
                                             x1, y1,
                                             outline='#4ff07a',
                                             tag='loop-'+str(l))
                text_w = self.controller.pages_font.measure(
                    modules[key]['type']) + 20
                self.canvas.create_text(
                    x0 + text_w/2,
                    y0 + 20,
                    font=self.controller.pages_font,
                    text=modules[key]['type'],
                    tags=('loop-'+str(l), 'type'+'-'+str(l)),
                    justify=tk.CENTER)
                text_w = self.controller.pages_font.measure(
                    modules[key]['condition']) + 20
                self.canvas.create_text(
                    x1 - text_w/2, 
                    y0 + 20, 
                    font = self.controller.pages_font, 
                    text = modules[key]['condition'], 
                    tags = ('loop-'+str(l), 'condition'+'-'+str(l)), 
                    justify = tk.CENTER)
                self.canvas.tag_bind('condition-'+str(l), 
                                 "<Double-1>", self.OnDoubleClick)
                self.canvas.tag_bind('type-'+str(l), 
                                 "<Double-1>", self.OnDoubleClick)
                self.loops.append({'type': modules[key]['type'],
                                   'condition': modules[key]['condition'],
                                   'mod': [],
                                   'coord': (x0, y0,
                                             x1, y1)})
                id_mod, disp_mod = self.place_modules(modules[key], id_mod, disp_mod)
            elif key not in disp_mod:
                # Display module
                self.add_module(key,
                                modules[key]['coordinates'][0][0],
                                modules[key]['coordinates'][0][1], 
                                iid = modules[key]['coordinates'][1])
                self.module_list[-1] = modules[key]['module_type']
                id_mod.append(modules[key]['coordinates'][1])
                disp_mod.append(key)
        self.module_list = [x for _, x in sorted(zip(id_mod, self.module_list))]
        self.canvas_startxy = [x for _, x in sorted(zip(id_mod, self.canvas_startxy))]
        return id_mod, disp_mod

    def draw_connection(self, modules, id_mod, disp_mod):
        for key in [key for key, val in modules.items() if type(val) == dict]:
            if modules[key]['class'] == 'loop':
                self.draw_connection(modules[key], id_mod, disp_mod)
            else:
                # Connect modules
                connect = list(modules[key]['coordinates'][2].keys())
                for p, parent in enumerate(modules[key]['parents']):
                    if not (parent[:4] == 'loop'):
                        # parent_id = modules[parent]['coordinates'][1]
                        parent_id = id_mod[np.where(np.array(disp_mod) == parent)[0][0]]
                        out, ins = modules[key]['coordinates'][2][connect[p]].split('-')
                        xout, yout, _ , _ = self.canvas.coords(out)
                        xins, yins, _, _ = self.canvas.coords(ins)
                        self.canvas.create_line(
                                    xout + self.cr,
                                    yout + self.cr,
                                    xins + self.cr,
                                    yins + self.cr,
                                    fill = "red", width = 2,
                                    arrow = tk.LAST, arrowshape = (12,10,5),
                                    tags = ('o'+str(parent_id),
                                          # 'o'+str(id_mod[-1]), 
                                          modules[key]['coordinates'][2][connect[p]]))
                        self.out_data.iloc[int(parent_id)][int(ins[1:])] = 1
                        self.connections[int(ins[1:])][
                            int(parent_id)] = out[0]+str(out[1:]) + '-' + ins[0]+str(ins[1:])
                    else:
                        self.loops[-1]['mod'].append(key)

    def reset(self):

        if not self.saved:
            msg = messagebox.askyesnocancel(
                'Info', 'Are you sure you want to reset the canvas?')
        else:
            msg = True
        if msg:
            self.canvas.delete(tk.ALL)  # Reset canvas

            if hasattr(self, 'entry'):
                self.entry.destroy()
            if hasattr(self, 'entry1'):
                self.entry1.destroy()
            if hasattr(self, 'entry2'):
                self.entry2.destroy()

            self.canvas_startxy = []
            self.out_data = pd.DataFrame()
            self.connections = {}
            self.modules = 0
            self.module_list = []
            self.module_names = []

            self.add_module('Initialiser', self.width/2, self.h, ini=True)
            self.add_module('Output', self.width/2,
                            self.height - self.h, out=True)

            self.draw = False
            self.loops = []
            self.drawLoop = False
            self.l = 0

    def check_quit(self):

        if not self.saved:
            response = messagebox.askokcancel(
                "Are you sure you want to leave?",
                "Do you want to leave the program without saving?")
            if response:
                if self.save_path not in [None, '']:
                    self.controller.XML.set(True)
                self.controller._show_frame("MainPage")
        else:
            if self.save_path not in [None, '']:
                self.controller.XML.set(True)
            self.controller._show_frame("MainPage")

# class ResizingCanvas(tk.Canvas):
#     def __init__(self,parent,**kwargs):
#         tk.Canvas.__init__(self,parent,**kwargs)
#         self.bind("<Configure>", self.on_resize)
#         self.height = self.winfo_reqheight()
#         self.width = self.winfo_reqwidth()

#     def on_resize(self,event):
#         # determine the ratio of old width/height to new width/height
#         wscale = float(event.width)/self.width
#         hscale = float(event.height)/self.height
#         self.width = event.width
#         self.height = event.height
#         # resize the canvas
#         self.config(width=self.width, height=self.height)
#         # rescale all the objects tagged with the "all" tag
#         self.scale("all",0,0,wscale,hscale)
