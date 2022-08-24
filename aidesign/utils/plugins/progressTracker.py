# Import the required libraries
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
from tkinter import messagebox

from aidesign.Data.xml_handler import XML_handler
from aidesign.utils.plugin_helpers import PluginSpecs

_PLUGIN_READABLE_NAMES = {"progress_tracker":"default","progressTracker":"alias","progress tracker":"alias"}
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                            "required_children": None}
_PLUGIN_REQUIRED_SETTINGS = {"id_done"}
_PLUGIN_OPTIONAL_SETTINGS = {}

class progressTracker(tk.Frame):
    """Canvas for the visualisation of the pipeline state."""
    
    def __init__(self, parent, controller, config:dict):
        
        """ Here we define the frame displayed for the plugin specification."""
        
        super().__init__(parent, bg = parent['bg'])
        self.bg = parent['bg']
        self.controller = controller
        self.s = XML_handler()
        
        script_dir = os.path.dirname(__file__)
        self.tk.call('wm','iconphoto', self.controller._w, ImageTk.PhotoImage(
            file = os.path.join(os.path.join(
                script_dir, 
                'resources', 
                'Assets', 
                'AIDIcon.ico'))))
        self.grid_rowconfigure(tuple(range(2)), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        frame1 = tk.Frame(self, bg = self.bg)
        self.frame2 = tk.Frame(self, bg = self.bg)
        frame3 = tk.Frame(self, bg = self.bg)
        self.frame4 = tk.Frame(self, bg = self.bg)
        
        # Create canvas
        self.width, self.height = 600, 600
        self.canvas = tk.Canvas(frame1, width=self.width, 
            height=self.height, background="white")
        self.canvas.pack(fill = tk.BOTH, expand = True, padx=(10,0), pady=10)
        
        self.w, self.h = 100, 50
        self.cr = 4
        """
        TODO: Implement clicking on canvas actions
        """
        # self.canvas.bind('<Button-1>', self.on_click)
        self.plugin = {}
        self.allWeHearIs = []
        
        self.upload()
        
        tk.Button(
            self.frame4, text = 'Next step', fg = 'white', bg = parent['bg'], 
            height = 3, width = 15, font = self.controller.pages_font, 
            command = self.check_quit).grid(column = 1, row = 26, sticky="news", pady=(0,10))
        
        self.save_path = ''
        self.saved = True
        frame1.grid(column=0, row=0, sticky="nsew")
        self.frame2.grid(column=1, row=0, sticky="ne")
        frame3.grid(column=0, row=1, sticky="swe")
        self.frame4.grid(column=1, row=1, sticky="sew")
        
        frame3.grid_columnconfigure(tuple(range(2)), weight=1)
        self.frame4.grid_columnconfigure(tuple(range(2)), weight=1)
        
    def class_list(self,value):
        """ Temporary fix """
        return value

    # def on_click(self, event):
    #     """ Passes the mouse click coordinates to the select function."""
    #     self.select(event.x, event.y)
        
    # def select(self, x: float, y:float):
    #     """ 
    #     Selects the module at the mouse location and updates the associated 
    #     plugins as well as the colours. 
    #     Blue means no plugin has been specified,
    #     Orange means the module is selected.
    #     Green means the plugin for this module is already set. 
    #     :param x: float type of module x coordinate
    #     :param y: float type of module y coordinate
    #     """
    #     self.selected = self.canvas.find_overlapping(
    #         x-5, y-5, x+5, y+5)
    #     if self.selected:
    #         if len(self.selected) > 2:
    #             self.canvas.selected = self.selected[-2]
    #         else:
    #             self.canvas.selected = self.selected[-1]
        
    #     if (self.m in self.plugin.keys()) and\
    #             (self.plugin[self.m].get() != 'None') and \
    #             (self.m not in self.id_done): # add
    #             self.id_done.append(self.m)
    #             self.s.append_plugin_to_module(self.plugin[self.m].get(),
    #                                              {**self.req_settings, **self.opt_settings},
    #                                              np.array(self.module_names)[self.m == np.array(self.id_mod)][0],
    #                                              True)
    #     if self.m in self.id_done and self.m > 1:
    #         self.canvas.itemconfig('p'+str(self.m), fill = '#46da63')
    #     else:
    #         self.canvas.itemconfig('p'+str(self.m), fill = self.bg)
        
    #     if len(self.canvas.gettags(self.canvas.selected)) > 0:
    #         if not (len(self.canvas.gettags(self.canvas.selected)[0].split('-')) > 1) and\
    #             not (self.canvas.gettags(self.canvas.selected)[0].split('-')[0] == 'loop'):
    #             self.m = int(self.canvas.gettags(self.canvas.selected)[0][1:])
    #         if self.m > 1:
    #             if self.m not in self.id_done and self.m > 1:
    #                 self.canvas.itemconfig('p'+str(self.m), fill = '#dbaa21')
    #             for widget in self.allWeHearIs:
    #                 widget.grid_remove()

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

    def add_module(self,boxName: str,x: float,y:float,ini = False,out = False):
        """ Creates a rectangular module with the corresponding text inside.
        
        :param boxName: name of the model
        :type boxName: str
        :param x: float type of module x coordinate
        :param y: float type of module y coordinate
        :param ini: bool type of whether the module corresponds to initialiser.
        :param out: bool type of whether the module corresponds to output.
        """
        if not ini and not out:
            tag = ('o'+str(self.modules),)
        else: #Make initialisation and output unmoveable
            tag = ('n0',)
        text_w = self.controller.pages_font.measure(boxName+'-00') + 10
        # Check module status
        if 'start' in self.controller.status[boxName]:
            if 'finish' in self.controller.status[boxName]:
                colour = '#46da63'
            else:
                colour = '#dbaa21'
        else:
            colour = self.bg
        
        self.canvas.create_rectangle(
            x - text_w/2 , 
            y - self.h/2, 
            x + text_w/2, 
            y + self.h/2, 
            tags = tag + ('p'+str(self.modules),), 
            fill = colour, 
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
        
        if not out:
            self.canvas.create_oval(
                x - self.cr, 
                y + self.h/2 - self.cr, 
                x + self.cr, 
                y + self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('d'+str(self.modules),))
            
        if not ini:
            self.canvas.create_oval(
                x - self.cr, 
                y - self.h/2 - self.cr, 
                x + self.cr, 
                y - self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('u'+str(self.modules),))
        
        if not out and not ini:
            self.canvas.create_oval(
                x - text_w/2 - self.cr, 
                y - self.cr, 
                x - text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('l'+str(self.modules),))
        
            self.canvas.create_oval(
                x + text_w/2 - self.cr, 
                y - self.cr, 
                x + text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('r'+str(self.modules),))
            
        self.canvas.startxy.append((x, y))
        self.connections[self.modules] = {}
        self.module_out(boxName)
        self.module_list.append(boxName)
        self.modules += 1

    def upload(self):
        """ Opens the XML file that was previously uploaded and places the 
        modules, loops and connections in the canvas."""
        
        filename = self.controller.output["xml_filename"]
        
        self.reset()

        self.s = XML_handler()
        self.s.load_XML(filename)
        # self.s._print_pretty(self.s.loaded_modules)
        modules = self.s.loaded_modules
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
        # self.select(x0, y0)

    def place_modules(self,modules: dict):
        """Places the modules in the dictionary in the canvas.
        :param modules: dict type of modules in the pipeline.
        """
        
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
        """ Resets the canvas and the stored information."""
        self.canvas.delete(tk.ALL) # Reset canvas
        
        if hasattr(self, 'newWindow') and (self.newWindow!= None):
            self.newWindow.destroy()
        
        self.canvas.startxy = []
        self.out_data = pd.DataFrame()
        self.connections = {}
        self.modules = 0
        self.module_list = []
        self.module_names = []
        
        self.add_module('Initialiser', self.width/2, self.h, ini = True)
        self.add_module('output', self.width/2, self.height - self.h, out = True)
    
        self.draw = False
        self.loops = []
        self.drawLoop = False
        self.l = 0
        self.id_done = [0,1]
        self.plugin = {}
        for widget in self.allWeHearIs:
                widget.grid_remove()
        self.allWeHearIs = []

    def check_quit(self):
        
        self.controller.destroy()
        

if __name__ == "__main__":
    app = progressTracker()
    app.mainloop()
