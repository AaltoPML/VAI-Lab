# Import the required libraries
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
from tkinter import messagebox

from aidesign.Settings.Settings_core import Settings

class pluginCanvas(tk.Frame):

    """ Creates a frame with a canvas and allows to include different modules
    for display which translate into new modules defined for the framework."""
    
    def __init__(self, parent, controller, config:dict):
        
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        
        super().__init__(parent, bg = parent['bg'])
        self.bg = parent['bg']
        self.controller = controller
        
        script_dir = os.path.dirname(__file__)
        self.tk.call('wm','iconphoto', self.controller._w, ImageTk.PhotoImage(
            file = os.path.join(os.path.join(
                script_dir, 
                'resources', 
                'Assets', 
                'AIDIcon.ico'))))
        # self.my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(
        #         script_dir, 
        #         'resources', 
        #         'Assets', 
        #         'AIDIcon_name.png')).resize((250, 200)))
        
        # self.my_label = tk.Label(self, image = self.my_img1, bg = parent['bg'])
        # self.my_label.grid(column = 5, row = 0)
        
        # Create canvas
        self.width, self.height = 600, 600
        self.canvas = tk.Canvas(self, width=self.width, 
            height=self.height, background="white")
        self.canvas.grid(row=0, column=0, columnspan=4, rowspan = 25, 
                         padx = 10, pady = 10)
        
        # Create module
        self.w, self.h = 100, 50
        self.cr = 4
        self.canvas.bind('<Button-1>', self.on_click)
        self.id_done = [0,1]
        self.plugin = {}
        self.allWeHearIs = []
        # self.l = 0 #number of loops
        # self.drawLoop = False
        # self.loops = []
        self.my_label = tk.Label(self, 
                    text = 
                    '',
                    pady= 10,
                    font = self.controller.title_font,
                    bg = self.bg,
                    fg = 'white')
        self.my_label.grid(column = 5,
                            row = 0, columnspan = 2)
        
        self.back_img = ImageTk.PhotoImage(Image.open(
            os.path.join(script_dir,
                         'resources', 
                         'Assets', 
                         'back_arrow.png')).resize((140, 60)))
        self.forw_img = ImageTk.PhotoImage(Image.open(
            os.path.join(script_dir,
                         'resources', 
                         'Assets',
                         'forw_arrow.png')).resize((140, 60)))
    
        tk.Button(
            self, text = 'Load Pipeline', fg = 'white', bg = parent['bg'], 
            height = 3, width = 15, font = self.controller.pages_font, 
            command = self.upload).grid(column = 0, row = 26, sticky = tk.SE)
        # tk.Button(
        #     self, text = 'Save', fg = 'white', bg = parent['bg'],
        #     height = 3, width = 15, font = self.controller.pages_font, 
        #     command = self.save_file).grid(column = 1, row = 10, sticky = tk.SW)
        # tk.Button(
        #     self, text = 'Reset', fg = 'white', bg = parent['bg'], 
        #     height = 3, width = 15, font = self.controller.pages_font, 
        #     command = self.reset).grid(column = 2, row = 10, sticky = tk.SE)
        tk.Button(
            self, text = 'Back to main', fg = 'white', bg = parent['bg'], 
            height = 3, width = 15, font = self.controller.pages_font, 
            command = self.check_quit).grid(column = 3, row = 26, sticky = tk.SW)
        
        self.save_path = ''
        self.saved = True

    def class_list(self,value):
        """ Temporary fix """
        return value

    def on_click(self, event):
        self.select(event.x, event.y)
        
    def select(self, x, y):
        """ Selects the module at the mouse location. """
        self.selected = self.canvas.find_overlapping(
            x-5, y-5, x+5, y+5)
        if self.selected:
            if len(self.selected) > 2:
                self.canvas.selected = self.selected[-2]
            else:
                self.canvas.selected = self.selected[-1]
        print(self.m, self.id_done)
        if self.m in self.id_done and self.m > 1:
            self.canvas.itemconfig('p'+str(self.m), fill = '#46da63')
        else:
            self.canvas.itemconfig('p'+str(self.m), fill = self.bg)
        
        if len(self.canvas.gettags(self.canvas.selected)) > 0:
            if(len(self.canvas.gettags(self.canvas.selected)[0].split('-')) > 1) and (
                self.canvas.gettags(self.canvas.selected)[0].split('-')[0] == 'loop'):
                self.m = int(self.canvas.gettags(self.canvas.selected)[0].split('-')[1])
            else:
                self.m = int(self.canvas.gettags(self.canvas.selected)[0][1:])
            
            if self.m not in self.id_done and self.m > 1:
                self.canvas.itemconfig('p'+str(self.m), fill = '#dbaa21')
            for widget in self.allWeHearIs:
                widget.grid_forget()
            
            self.display_buttons()
            module_number = self.id_mod.index(self.m)
            print(module_number)
            
            if module_number == len(self.id_mod)-1:
                self.button_forw.grid_forget()
                self.button_forw = tk.Button(
                    self, text = 'Finnish', bg = self.bg, 
                    font = self.controller.pages_font,
                    fg = 'white', height = 3, width = 15,
                    command = self.check_quit).grid(column = 6,row = 26)
            else:
                pCoord = self.canvas.coords('p'+str(self.id_mod[module_number+1]))
                self.button_forw = tk.Button(
                self, image = self.forw_img, bg = self.bg, 
                command = lambda: self.select(
                    pCoord[0], pCoord[1]))
                self.button_forw.grid(column = 6,row = 26)
            if module_number < 3:
                self.button_back = tk.Button(
                    self, image = self.back_img, bg = self.bg, 
                    state = tk.DISABLED).grid(column = 5,row = 26)
            else:
                mCoord = self.canvas.coords('p'+str(self.id_mod[module_number-1]))
                self.button_back = tk.Button(
                    self, image = self.back_img, bg = self.bg, 
                    command = lambda: self.select(
                        mCoord[0], mCoord[1])).grid(column = 5,row = 26)
        
        if (self.plugin[self.m].get() != 'None') and \
            (self.m not in self.id_done):
            print('Someone joined us!')
            self.id_done.append(self.m)
        self.saved = False

    def display_buttons(self):
        module = self.module_list[self.m == self.id_mod]
        name = self.canvas.itemcget('t'+str(self.m), 'text')
        self.my_label.config(text = 'Choose a plugin for the '+name+' module')
        
        plugins = ['GP', 'SVM', 'MLP', 'Ridge', 'Lasso', 'CCA', 'RF']
        if self.m not in self.plugin:
            self.plugin[self.m] = tk.StringVar()
            self.plugin[self.m].set(None)
        self.allWeHearIs = []
        for p, plug in enumerate(plugins):
            rb = tk.Radiobutton(self, text = plug, fg = 'white', bg = self.bg,
                height = 3, width = 20, var = self.plugin[self.m], 
                selectcolor = 'black', value = plug,
                    font = self.controller.pages_font)
            rb.grid(column = 5+ (p%2 != 0), row = int(p/2)+1)
            self.allWeHearIs.append(rb)

    
    def module_out(self, name):
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
        self.canvas.itemconfig('t'+str(self.modules), text = name_list[-1])
        values = self.out_data.values
        values = np.vstack((
                    np.hstack((values, np.zeros((values.shape[0],1)))),
                    np.zeros((1, values.shape[0]+1))))
        self.out_data = pd.DataFrame(values, 
                                     columns = name_list, 
                                     index = name_list)
        self.module_names.append(name_list[-1])

    def add_module(self, boxName, x, y, ini = False, out = False):
        """ Creates a rectangular module with the corresponding text inside.
        
        :param boxName: name of the model
        :type boxName: str
        """
        if not ini and not out:
            tag = ('o'+str(self.modules),)
        else: #Make initialisation and output unmoveable
            tag = ('n0',)
        text_w = self.controller.pages_font.measure(boxName+'-00') + 10
        self.canvas.create_rectangle(
            x - text_w/2 , 
            y - self.h/2, 
            x + text_w/2, 
            y + self.h/2, 
            tags = tag + ('p'+str(self.modules),), 
            fill = self.bg, 
            width = 3,
            # activefill = '#dbaa21'
            )
        self.canvas.create_text(
            x, 
            y, 
            font = self.controller.pages_font, 
            text = boxName, 
            tags = tag + ('t'+str(self.modules),), 
            fill = '#d0d4d9', 
            justify = tk.CENTER)
        # self.canvas.tag_bind('t'+str(self.modules), 
        #                      "<Double-1>", self.OnDoubleClick)
        if not out:
            self.canvas.create_oval(
                x - self.cr, 
                y + self.h/2 - self.cr, 
                x + self.cr, 
                y + self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('d'+str(self.modules),))
            # self.canvas.tag_bind('d'+str(self.modules), 
            #                      "<Button-1>", self.join_modules)
            
        if not ini:
            self.canvas.create_oval(
                x - self.cr, 
                y - self.h/2 - self.cr, 
                x + self.cr, 
                y - self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('u'+str(self.modules),))
            # self.canvas.tag_bind('u'+str(self.modules), 
            #                      "<Button-1>", self.join_modules)
        
        if not out and not ini:
            self.canvas.create_oval(
                x - text_w/2 - self.cr, 
                y - self.cr, 
                x - text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('l'+str(self.modules),))
            # self.canvas.tag_bind('l'+str(self.modules), 
            #                      "<Button-1>", self.join_modules)
        
            self.canvas.create_oval(
                x + text_w/2 - self.cr, 
                y - self.cr, 
                x + text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('r'+str(self.modules),))
            # self.canvas.tag_bind('r'+str(self.modules), 
            #                      "<Button-1>", self.join_modules)
        self.canvas.startxy.append((x, 
                                    y))
        self.connections[self.modules] = {}
        self.module_out(boxName)
        self.module_list.append(boxName)
        self.modules += 1

    def upload(self):
        
        filename = self.controller.output["xml_filename"]
        
        self.reset()

        s = Settings()
        s.load_XML(filename)
        s._print_pretty(s.loaded_modules)
        modules = s.loaded_modules
        modout = modules['output']
        del modules['Initialiser'], modules['output'] # They are generated when resetting
        self.disp_mod = ['Initialiser', 'output']
        self.id_mod = [0, 1]
        
        # Place the modules
        self.place_modules(modules)
        connect = list(modout['coordinates'][2].keys())
        for p, parent in enumerate(modout['parents']):
                parent_id = self.id_mod[np.where(np.array(self.disp_mod) == parent)[0][0]]
                out, ins = modout['coordinates'][2][connect[p]].split('-')
                xout, yout, _ , _ = self.canvas.coords(out[0]+str(parent_id))
                xins, yins, _, _ =self.canvas.coords(ins[0]+str(1))
                self.canvas.create_line(
                            xout + self.cr, 
                            yout + self.cr, 
                            xins + self.cr, 
                            yins + self.cr,
                            fill = "red", 
                            arrow = tk.LAST, 
                            tags = ('o'+str(parent_id), 
                                  'o'+str(1), modout['coordinates'][2][connect[p]]))
                self.out_data.iloc[int(parent_id)][1] = 1
                self.connections[1][
                    int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(1)
        self.m = self.id_mod[2]
        x0, y0, x1, y1 = self.canvas.coords('p'+str(self.m))
        self.select(x0, y0)

    def place_modules(self, modules):
        # Place the modules
        for key in [key for key, val in modules.items() if type(val) == dict]:
            if modules[key]['class'] == 'loop':
                # Extracts numbers from string
                l = int(''.join(map(str, list(filter(str.isdigit, modules[key]['name'])))))
                x0, y0, x1, y1 = modules[key]['coordinates']
                self.canvas.create_rectangle(x0, y0, 
                                             x1, y1, 
                                             outline = '#4ff07a',
                                             tag = 'loop-'+str(l))
                text_w = self.controller.pages_font.measure(modules[key]['type']) + 20
                self.canvas.create_text(
                    x0 + text_w/2, 
                    y0 + 20, 
                    font = self.controller.pages_font, 
                    text = modules[key]['type'], 
                    tags = ('loop-'+str(l), 'type'+'-'+str(l)), 
                    justify = tk.CENTER)
                text_w = self.controller.pages_font.measure(modules[key]['condition']) + 20
                self.canvas.create_text(
                    x1 - text_w/2, 
                    y0 + 20, 
                    font = self.controller.pages_font, 
                    text = modules[key]['condition'], 
                    tags = ('loop-'+str(l), 'condition'+'-'+str(l)), 
                    justify = tk.CENTER)
                self.loops.append({'type': modules[key]['type'],
                                   'condition': modules[key]['condition'],
                                   'mod': [], 
                                   'coord': (x0, y0, 
                                             x1, y1)})
                self.place_modules(modules[key])
            else:
                # Display module
                self.add_module(key,
                                modules[key]['coordinates'][0][0],
                                modules[key]['coordinates'][0][1])
                self.module_list[-1] = modules[key]['module_type']
                self.id_mod.append(modules[key]['coordinates'][1])
                connect = list(modules[key]['coordinates'][2].keys())
                
                # Connect modules
                for p, parent in enumerate(modules[key]['parents']):
                    if not (parent[:4] == 'loop'):
                        parent_id = self.id_mod[np.where(np.array(self.disp_mod) == parent)[0][0]]
                        out, ins = modules[key]['coordinates'][2][connect[p]].split('-')
                        xout, yout, _ , _ = self.canvas.coords(out[0]+str(parent_id))
                        xins, yins, _, _ =self.canvas.coords(ins[0]+str(self.id_mod[-1]))
                        self.canvas.create_line(
                                    xout + self.cr, 
                                    yout + self.cr, 
                                    xins + self.cr, 
                                    yins + self.cr,
                                    fill = "red", 
                                    arrow = tk.LAST, 
                                    tags = ('o'+str(parent_id), 
                                          'o'+str(self.id_mod[-1]), modules[key]['coordinates'][2][connect[p]]))
                        self.out_data.iloc[int(parent_id)][int(self.id_mod[-1])] = 1
                        self.connections[int(self.id_mod[-1])][
                            int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(self.id_mod[-1])
                    else:
                        self.loops[-1]['mod'].append(key)
                self.disp_mod.append(key)

    def reset(self):
        
        # if not self.saved:
        #     msg = messagebox.askyesnocancel(
        #         'Info', 'Are you sure you want to reset the canvas?')
        # else:
        #     msg = True
        # if msg:
        self.canvas.delete(tk.ALL) # Reset canvas
        
        if hasattr(self, 'entry'):
            self.entry.destroy()
        if hasattr(self, 'entry1'):
            self.entry1.destroy()
        if hasattr(self, 'entry2'):
            self.entry2.destroy()
            
        self.canvas.startxy = []
        self.out_data = pd.DataFrame()
        self.connections = {}
        self.modules = 0
        self.module_list = []
        self.module_names = []
        
        self.add_module('Initialiser', self.width/2, self.h, ini = True)
        self.add_module('Output', self.width/2, self.height - self.h, out = True)
    
        self.draw = False
        self.loops = []
        self.drawLoop = False
        self.l = 0
        self.id_done = [0,1]
        self.plugin = {}
        self.allWeHearIs = []
            
    def check_quit(self):
        
        if not len(self.id_done) == len(self.id_mod):
            response = messagebox.askokcancel(
                "Exit", 
                "There are some unspecified plugins. Are you sure you want to leave?")
            if response:
                self.reset()
                self.canvas.delete(tk.ALL)
                self.saved = True
                self.controller._show_frame("MainPage")
        else:
            self.reset()
            self.canvas.delete(tk.ALL)
            self.saved = True
            self.controller._show_frame("MainPage")

if __name__ == "__main__":
    app = pluginCanvas()
    app.mainloop()