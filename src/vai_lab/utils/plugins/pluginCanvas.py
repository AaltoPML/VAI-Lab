from vai_lab.Data.xml_handler import XML_handler
from vai_lab._plugin_helpers import PluginSpecs
from vai_lab._import_helper import get_lib_parent_dir, import_plugin_absolute

import os
import numpy as np
import pandas as pd
from inspect import getmembers, isfunction, ismethod, signature
from functools import reduce

from typing import Dict, List
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfilename

_PLUGIN_READABLE_NAMES = {"plugin_canvas": "default",
                          "pluginCanvas": "alias",
                          "plugin canvas": "alias"}         # type:ignore
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                          "required_children": None}        # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                              # type:ignore


class pluginCanvas(tk.Frame):
    """Canvas for graphical specification of plugins"""

    def __init__(self, parent, controller, config: dict):
        """ Here we define the frame displayed for the plugin specification."""

        super().__init__(parent, bg=parent['bg'])
        self.bg = parent['bg']
        self.parent = parent
        self.controller = controller
        self.m: int
        self.w, self.h = 100, 50
        self.cr = 4
        self.id_done = [0, 1]
        self.id_mod:List[int] = [0, 1]
        self.out_data = pd.DataFrame()
        self.plugin: Dict[int, tk.StringVar] = {}
        self.dataType: Dict[int, tk.StringVar] = {}
        self.allWeHearIs: List[tk.Radiobutton] = []
        self.out_data_xml: List[int, tk.StringVar] = []
        self.out_data_list: List[int, tk.StringVar] = []
        if not self.controller._debug:
            self._setup_frame()

    def _setup_frame(self):
        script_dir = get_lib_parent_dir()
        self.tk.call('wm', 'iconphoto', self.controller._w, ImageTk.PhotoImage(
            file=os.path.join(os.path.join(
                script_dir,
                'utils',
                'resources',
                'Assets',
                'VAILabsIcon.ico'))))
        # self.grid_rowconfigure(tuple(range(5)), weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(self, bg=self.bg)
        self.frame2 = tk.Frame(self, bg=self.bg)
        self.framex = tk.Frame(self, bg=self.bg)
        frame3 = tk.Frame(self, bg=self.bg)
        self.frame4 = tk.Frame(self, bg=self.bg)

        # Create canvas
        self.width, self.height = 700, 700
        self.canvas = tk.Canvas(frame1, width=self.width,
                                height=self.height, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

        self.canvas.bind('<Button-1>', self.on_click)
        

        self.my_label = tk.Label(self.frame2,
                                 text='',
                                 pady=10,
                                 font=self.controller.title_font,
                                 bg=self.bg,
                                 fg='white',
                                 anchor=tk.CENTER)
        self.my_label.grid(column=0,
                           row=0, columnspan=3, padx=10)

        self.back_img = ImageTk.PhotoImage(Image.open(
            os.path.join(script_dir,
                         'utils',
                         'resources',
                         'Assets',
                         'back_arrow.png')).resize((140, 60)))
        self.forw_img = ImageTk.PhotoImage(Image.open(
            os.path.join(script_dir,
                         'utils',
                         'resources',
                         'Assets',
                         'forw_arrow.png')).resize((140, 60)))

        ww = int(self.width/40)
        tk.Button(
            frame3, text='Load Pipeline', fg='white', bg=self.bg,
            height=3, width=ww, font=self.controller.pages_font,
            command=self.upload).grid(column=0, row=0, sticky="news",
                                      padx=(10, 0), pady=(0, 10))
        tk.Button(
            frame3, text='Back to main', fg='white', bg=self.bg,
            height=3, width=ww, font=self.controller.pages_font,
            command=self.check_quit).grid(column=1, row=0, sticky="news", pady=(0, 10))

        self.frame_canvas = tk.Canvas(
            self.framex, bg=self.bg, bd=0, highlightthickness=0)
        self.tree_scrolly = tk.Scrollbar(
            self.framex, command=self.frame_canvas.yview)
        self.tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_scrollx = tk.Scrollbar(
            self.framex, command=self.frame_canvas.xview, orient='horizontal')
        self.tree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)

        self.save_path = ''
        self.saved = True
        frame1.grid(column=0, row=0, rowspan=5, sticky="nsew")
        self.frame2.grid(column=1, row=0, sticky="new", padx=(10, 0))
        frame3.grid(column=0, row=5, sticky="nswe")
        self.frame4.grid(column=1, row=5, sticky="nsew")

        # self.frame2.grid_columnconfigure(tuple(range(2)), weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        frame3.grid_columnconfigure(tuple(range(2)), weight=2)
        # frame3.grid_columnconfigure(2, weight=2)
        self.frame4.grid_columnconfigure(tuple(range(2)), weight=2)
        # self.frame4.grid_columnconfigure(2, weight=2)

    def class_list(self, value):
        """ Temporary fix """
        return value

    def on_click(self, event):
        """ Passes the mouse click coordinates to the select function."""
        self.select(event.x, event.y)

    def select(self, x: float, y: float):
        """ 
        Selects the module at the mouse location and updates the associated 
        plugins as well as the colours. 
        Blue means no plugin has been specified,
        Orange means the module is selected.
        Green means the plugin for this module is already set. 
        :param x: float type of module x coordinate
        :param y: float type of module y coordinate
        """
        self.selected = self.canvas.find_overlapping(
            x-5, y-5, x+5, y+5)
        self.canvas_selected: int
        if self.selected:
            if len(self.selected) > 2:
                self.canvas_selected = self.selected[-2]
            else:
                self.canvas_selected = self.selected[-1]

        self.check_updated()

        if self.m in self.id_done and self.m > 0:
            self.canvas.itemconfig('p'+str(self.m), fill='#46da63')
        else:
            self.canvas.itemconfig('p'+str(self.m), fill=self.bg)

        if len(self.canvas.gettags(self.canvas_selected)) > 0:
            if not (len(self.canvas.gettags(self.canvas_selected)[0].split('-')) > 1) and\
                    not (self.canvas.gettags(self.canvas_selected)[0].split('-')[0] == 'loop'):
                self.m = int(self.canvas.gettags(self.canvas_selected)[0][1:])
            if self.m > 0: #> 1:
                if self.m not in self.id_done:
                    self.canvas.itemconfig('p'+str(self.m), fill='#dbaa21')
                for widget in self.allWeHearIs:
                    widget.grid_remove()
                if self.m > 1:
                    self.reset_sidecheck()
                    self.display_buttons()
                else:
                    self.reset_sidepanel()
                    self.display_checklist()
                module_number = self.id_mod.index(self.m)
                if not hasattr(self, 'button_forw'):
                    if module_number == 1:
                        self.button_forw = tk.Button(
                            self.frame4, text='Finish', bg=self.bg,
                            font=self.controller.pages_font,
                            fg='white', height=3, width=15,
                            command=self.finish, state=tk.NORMAL, image='')
                    elif module_number == len(self.id_mod)-1:
                        pCoord = self.canvas.coords(
                            'p'+str(self.id_mod[1]))
                        self.button_forw = tk.Button(
                            self.frame4, image=self.forw_img, bg=self.bg,
                            command=lambda: self.select(
                                pCoord[0], pCoord[1]), state=tk.NORMAL)
                    else:
                        pCoord = self.canvas.coords(
                            'p'+str(self.id_mod[module_number+1]))
                        self.button_forw = tk.Button(
                            self.frame4, image=self.forw_img, bg=self.bg,
                            command=lambda: self.select(
                                pCoord[0], pCoord[1]), state=tk.NORMAL)
                    self.button_forw.grid(
                        column=1, row=0, sticky="news", pady=(0, 10), padx=(0, 10))
                    if module_number == 1:
                        mCoord = self.canvas.coords(
                            'p'+str(self.id_mod[-1]))
                        self.button_back = tk.Button(
                            self.frame4, image=self.back_img, bg=self.bg,
                            command=lambda: self.select(
                                mCoord[0], mCoord[1]), state=tk.NORMAL)
                    elif module_number < 3:
                        self.button_back = tk.Button(
                                self.frame4, image=self.back_img, bg=self.bg,
                                state=tk.DISABLED)
                    else:
                        mCoord = self.canvas.coords(
                            'p'+str(self.id_mod[module_number-1]))
                        self.button_back = tk.Button(
                            self.frame4, image=self.back_img, bg=self.bg,
                            command=lambda: self.select(
                                mCoord[0], mCoord[1]), state=tk.NORMAL)
                    self.button_back.grid(
                        column=0, row=0, sticky="news", pady=(0, 10))
                else:
                    if module_number == 1:
                        self.button_forw.config(text='Finish', bg=self.bg,
                                                font=self.controller.pages_font,
                                                fg='white', height=3, width=15,
                                                command=self.finish, state=tk.NORMAL, image='')
                    elif module_number == len(self.id_mod)-1:
                        pCoord = self.canvas.coords(
                            'p'+str(self.id_mod[1]))
                        self.button_forw.config(image=self.forw_img, bg=self.bg,
                                                command=lambda: self.select(
                                                    pCoord[0], pCoord[1]), text='', state=tk.NORMAL)
                    else:
                        pCoord = self.canvas.coords(
                            'p'+str(self.id_mod[module_number+1]))
                        self.button_forw.config(image=self.forw_img, bg=self.bg,
                                                command=lambda: self.select(
                                                    pCoord[0], pCoord[1]), text='', state=tk.NORMAL)
                    if module_number == 1:
                        mCoord = self.canvas.coords(
                            'p'+str(self.id_mod[-1]))
                        self.button_back.config(image=self.back_img, bg=self.bg,
                                                command=lambda: self.select(
                                                    mCoord[0], mCoord[1]), text='', state=tk.NORMAL)
                    elif module_number < 3:
                        self.button_back.config(image=self.back_img, bg=self.bg,
                                                state=tk.DISABLED, text='')
                    else:
                        mCoord = self.canvas.coords(
                            'p'+str(self.id_mod[module_number-1]))
                        self.button_back.config(image=self.back_img, bg=self.bg,
                                                command=lambda: self.select(
                                                    mCoord[0], mCoord[1]), text='', state=tk.NORMAL)
            else:          # If user clicks on Initialiser
                self.reset_sidepanel()
                if hasattr(self, 'button_forw'):
                    self.button_back.config(image=self.back_img, bg=self.bg,
                                            state=tk.DISABLED, text='')
                    pCoord = self.canvas.coords('p'+str(self.id_mod[2]))
                    self.button_forw.config(image=self.forw_img, bg=self.bg,
                                            command=lambda: self.select(
                                                pCoord[0], pCoord[1]), text='', state=tk.NORMAL)               
    def reset_sidepanel(self):
        """ Removes information from the panel to the side of the canvas.
        """
        self.my_label.config(text='')
        for widget in self.allWeHearIs:
            widget.grid_remove()
        for widget in self.radio_label:
            widget.grid_remove()
        self.reset_sidecheck()
    
    def reset_sidecheck(self):
        if hasattr(self, 'frame_tree'):
            self.frame_tree.grid_remove()
        if hasattr(self, 'frame_path'):
            self.frame_path.grid_remove()

    def finish(self):
        """ Calls function check_quit.
        Before that, it checks if the current module plugins have been changed 
        and, if so, updates their information in the XML_handler class.
        """
        self.check_updated()
        self.check_quit()

    def check_updated(self):
        """ Checks if the current plugin exists and stores/updates the plugin options. 
        It also cheks if the output data has been modfied and stores/updates the 
        information accordingly.
        """
        if (self.m in self.plugin.keys()) and\
                (self.plugin[self.m].get() != 'None'):  # add
            self.id_done.append(self.m)
            self.xml_handler.append_plugin_to_module(
                self.plugin[self.m].get(),
                self.merge_dicts(self.req_settings, self.opt_settings),
                self.meths_sort,
                self.plugin_inputData.get(),
                np.array(self.module_names)[self.m == np.array(self.id_mod)][0],
                True)

        elif len(set([elem.get() for elem in self.out_data_list if len(elem.get())>1]) 
                 ^ set(self.out_data_xml)) > 0 :
            self.out_data_xml = [elem.get() for elem in self.out_data_list if len(elem.get())>1]
            self.id_done.append(self.m)

            if os.path.normpath(get_lib_parent_dir()) == os.path.normpath(os.path.commonpath([self.path_out, get_lib_parent_dir()])):
                rel_path = os.path.join('.', os.path.relpath(self.path_out,
                                                os.path.commonpath([self.path_out, get_lib_parent_dir()])))
            else:
                rel_path = self.path_out

            self.xml_handler.append_plugin_to_module(
                'Output',
                {'__init__': {'outdata': self.out_data_xml,
                              'outpath': rel_path}},
                [],
                None,
                np.array(self.module_names)[self.m == np.array(self.id_mod)][0],
                True)

    def merge_dicts(self, a, b, path = None):
        "merges b into a"
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge_dicts(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass # same leaf value
                else:
                    raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a
    
    def display_buttons(self):
        """ Updates the displayed radiobuttons and the description windows.
        It loads the information corresponding to the selected module (self.m)
        and shows the available plugins and their corresponding descriptions.
        """
        module = np.array(self.module_list)[self.m == np.array(self.id_mod)][0]
        name = self.canvas.itemcget('t'+str(self.m), 'text')
        ps = PluginSpecs()
        plugin_list = list(ps.class_names[module].values())
        plugin_list.append('Custom')
        descriptions = list(ps.class_descriptions[module].values())
        descriptions.append('User specified plugin')
        type_list = np.array([x.get('Type', None)
                             for x in list(ps.module_options[module].values())])
        type_list = np.append(type_list, None)
        text = ''
        if module.lower() == 'modelling':
            text = '\nPluggins in white correspond to '+self.controller.output_type
        self.my_label.config(
            text='Choose a plugin for the '+name+' module'+text)
        if self.m not in self.plugin:
            self.plugin[self.m] = tk.StringVar()
            self.plugin[self.m].set(None)
        self.allWeHearIs = []

        try:
            for frame in self.framexx:
                frame.grid_forget()
                frame.destroy()
            self.framexx = []
        except AttributeError:
            self.framexx = []
        framexx_name = np.array([])
        framexx_i = []
        self.radio_label = []
        values = np.append(np.unique(type_list[type_list != None]), 'other') if not any(
            type_list == 'other') else np.unique(type_list[type_list != None])
        for i, t in enumerate(values):
            self.framexx.append(tk.Frame(self.framep, bg=self.bg))
            framexx_name = np.append(
                framexx_name, t if t is not None else 'other')
            framexx_i.append(0)
            self.radio_label.append(tk.Label(self.framexx[-1],
                             text=framexx_name[-1].capitalize(),
                             pady=10,
                             font=self.controller.title_font,
                             bg=self.bg,
                             fg='white'))
            self.radio_label[-1].grid(column=0,
                       row=0, padx=(10, 0), sticky='nw')
            self.framexx[-1].grid(column=0, row=i, sticky="nsew")
        unsupervised = ['clustering', 'RL']
        for p, plug in enumerate(plugin_list):
            if module.lower() == 'modelling' and p < len(plugin_list)-1:
                colour = 'white' if type_list[p] == self.controller.output_type or (
                    self.controller.output_type == 'unsupervised' and type_list[p] in unsupervised) else 'grey'
            else:
                colour = 'white'
            frame_idx = np.where(framexx_name == type_list[p])[
                0][0] if type_list[p] in framexx_name else np.where(framexx_name == 'other')[0][0]
            rb = tk.Radiobutton(self.framexx[frame_idx], text=plug, fg=colour, bg=self.bg,
                                height=3, var=self.plugin[self.m],
                                selectcolor='black', value=plug, justify=tk.LEFT,
                                font=self.controller.pages_font, command=self.optionsWindow)
            rb.grid(column=int(framexx_i[frame_idx] % 2 != 0),
                    row=int(framexx_i[frame_idx]/2)+1,
                    sticky='w',
                    padx=(10, 0))
            framexx_i[frame_idx] += 1
            self.CreateToolTip(rb, text=descriptions[p])
            self.allWeHearIs.append(rb)

    def display_checklist(self):
        """ Updates the displayed tree to the left of canvas.
         Used to specify the output data and files. """
        self.my_label.config(
            text='Indicate which module\'s output data\nshould be saved:')
        dataSources = [i for j, i in enumerate(self.module_names) if j != 1]
        self.frame_tree = tk.Frame(self.frame_canvas, bg=self.bg)
        self.frame_tree.grid(column=0, row=0, sticky="new", padx=(10, 0))
        for c, choice in enumerate(dataSources):
            cb = tk.Checkbutton(self.frame_tree, var=self.out_data_list[c], text=choice,
                                onvalue=choice, offvalue="",
                                pady=10,
                                font=self.controller.pages_font,
                                bg=self.bg,
                                fg='white',
                                selectcolor=self.bg,
                                anchor='w',
                                width=20, 
                                background=self.frame_canvas.cget("background")
            )
            cb.grid(row=c, column=0)
            if c == len(dataSources)-1:
                cb.select()
        self.frame_path = tk.Frame(self.frame_canvas, bg=self.bg)
        self.frame_path.grid(column=0, row=1, sticky="new", padx=(10, 0))
        self.my_label = tk.Label(self.frame_path,
                                 text='Indicate the output file name:',
                                 pady=10,
                                 font=self.controller.title_font,
                                 bg=self.bg,
                                 fg='white',
                                 anchor=tk.CENTER)
        self.my_label.grid(column=0,
                           row=0, columnspan=2, padx=10)
        tk.Button(self.frame_path,
                    text="Browse",
                    command=self.upload_file
                    ).grid(column=0, row=1)
        width = 63
        self.path_out = os.path.join(get_lib_parent_dir(),'examples','results','output.pkl')
        filename = '...' + \
            self.path_out[-width +
                     3:] if self.path_out and len(self.path_out) > width else self.path_out
        self.label_list = tk.Label(self.frame_path, text=filename,
                                pady=10,
                                padx=10,
                                font=self.controller.pages_font,
                                fg='white', 
                                bg=self.bg
                                )
        self.label_list.grid(column=1, row=1)
    
    def upload_file(self):
        """ Asks for a file and stores the path and displays it.
        """
        filename = asksaveasfilename(initialdir=os.path.join(get_lib_parent_dir(),'examples','results'),
                                    title='Select an output file',
                                    defaultextension='.pkl', 
                                    filetypes=[('Pickle file', '.pkl')])
        if filename is not None:
            self.path_out = filename
            width = 63
            filename = '...' + \
                filename[-width +
                        3:] if filename and len(filename) > width else filename
            self.label_list.config(text=filename)

    def getCheckedItems(self):
            values = []
            for var in self.vars:
                value =  var.get()
                if value:
                    values.append(value)
            return values

    def optionsWindow(self):
        """ Function to create a new window displaying the available options 
        of the selected plugin."""

        module = np.array(self.module_list)[self.m == np.array(self.id_mod)][0]
        ps = PluginSpecs()
        file_name = os.path.split(ps.find_from_class_name(self.plugin[self.m].get())['_PLUGIN_DIR'])[-1]
        avail_plugins = ps.available_plugins[module][file_name]
        plugin = import_plugin_absolute(globals(),
                                        avail_plugins["_PLUGIN_PACKAGE"],
                                        avail_plugins["_PLUGIN_CLASS_NAME"])
        # Update required and optional settings for the plugin
        self.req_settings = {'__init__': ps.required_settings[module][self.plugin[self.m].get()]}
        self.opt_settings = {'__init__': ps.optional_settings[module][self.plugin[self.m].get()]}
        # Tries to upload the settings from the actual library 
        try:
            self.plugin_ini = plugin(ini = True)
            meth_req, meth_opt = self.getArgs(self.plugin_ini.model.__init__)
            if meth_req is not None:
                self.req_settings['__init__'] = {**self.req_settings['__init__'], **meth_req}
            if meth_opt is not None:
                self.opt_settings['__init__'] = {**self.opt_settings['__init__'], **meth_opt}
            # Only including mapped methods/functions
            meth_list = [meth[0].split('_plugin')[0] for meth in getmembers(plugin(ini=True), isfunction) if meth[0][0] != '_']
        except Exception as exc:
            meth_list = []


        self.meths_sort = []
        self.method_inputData = {}
        self.default_inputData = {}

        if hasattr(self, 'newWindow') and (self.newWindow != None):
            self.newWindow.destroy()
        self.newWindow = tk.Toplevel(self.controller)
        # Window options
        self.newWindow.title(self.plugin[self.m].get()+' plugin options')
        script_dir = get_lib_parent_dir()
        self.tk.call('wm', 'iconphoto', self.newWindow, ImageTk.PhotoImage(
            file=os.path.join(os.path.join(
                script_dir,
                'utils',
                'resources',
                'Assets',
                'VAILabsIcon.ico'))))
        # self.newWindow.geometry("350x400")


        frame1 = tk.Frame(self.newWindow)
        frame2 = tk.Frame(self.newWindow)
        frame3 = tk.Frame(self.newWindow)
        frame4 = tk.Frame(self.newWindow)
        frame5 = tk.Frame(self.newWindow)
        frame6 = tk.Frame(self.newWindow, highlightbackground="black", highlightthickness=1)

        # Print settings
        tk.Label(frame1,
                    text="Please indicate your desired options for the plugin.", anchor=tk.N, justify=tk.LEFT).pack(expand=True)
        
        style = ttk.Style()
        style.configure(
            "Treeview", background='white', foreground='white',
            rowheight=25, fieldbackground='white',
            # font=self.controller.pages_font
            )
        style.configure("Treeview.Heading", 
        # font=self.controller.pages_font
        )
        style.map('Treeview', background=[('selected', 'grey')])

        # Show method selection if there is any
        if len(meth_list) > 0:
            frame21 = tk.Frame(self.newWindow)
            frameButt = tk.Frame(frame3)
            frameDrop = tk.Frame(frame3, highlightbackground="black", highlightthickness=1)

            tk.Label(frame21,
                    text="Add your desired methods in your required order.", anchor=tk.N, justify=tk.LEFT).pack(expand=True)

            self.meth2add = tk.StringVar(frameDrop)
            dropDown = tk.ttk.OptionMenu(frameDrop, self.meth2add, meth_list[0], *meth_list)
            style.configure("TMenubutton", background="white")
            dropDown["menu"].configure(bg="white")
            dropDown.grid(row=0,column=0)

            tk.Button(frameButt, text='Add', command=self.addMeth).grid(row=0,column=0)
            tk.Button(frameButt, text='Delete', command=self.deleteMeth).grid(row=0,column=1)
            tk.Button(frameButt, text='Up', command=lambda: self.moveMeth(-1)).grid(row=0,column=2)
            tk.Button(frameButt, text='Down', command=lambda: self.moveMeth(+1)).grid(row=0,column=3)

            frame21.grid(column=0, row=2, sticky="ew")
            frameButt.grid(column=1, row=0, sticky="w")
            frameDrop.grid(column=0, row=0)

        self.r = 1
        self.tree = self.create_treeView(frame2, ['Name', 'Value'])
        self.tree.insert(parent='', index='end', iid='__init__', text='', values=tuple(['__init__', '']), 
                            tags=('meth','__init__'))            
        self.fill_treeview(self.req_settings['__init__'], self.opt_settings['__init__'], '__init__')

        tk.Label(frame5,
                    text="Indicate which plugin's output data should be used as input", anchor=tk.N, justify=tk.LEFT).pack(expand=True)
        
        current = np.where(self.m == np.array(self.id_mod))[0][0]
        dataSources = [i for j, i in enumerate(self.module_names) if j not in [1,current]]

        self.plugin_inputData = tk.StringVar(frame6)
        dropDown = tk.ttk.OptionMenu(frame6, self.plugin_inputData, dataSources[current-2], *dataSources)
        style.configure("TMenubutton", background="white")
        dropDown["menu"].configure(bg="white")
        dropDown.pack()

        self.finishButton = tk.Button(
            frame4, text='Finish', command=self.removewindow)
        self.finishButton.grid(
            column=1, row=0, sticky="es", pady=(0, 10), padx=(0, 10))
        self.finishButton.bind(
            "<Return>", lambda event: self.removewindow())
        self.newWindow.protocol('WM_DELETE_WINDOW', self.removewindow)

        frame1.grid(column=0, row=0, sticky="ew")
        frame2.grid(column=0, row=1, sticky="nswe", pady=10, padx=10)
        frame3.grid(column=0, row=3, pady=10, padx=10)
        frame4.grid(column=0, row=20, sticky="se")
        frame5.grid(column=0, row=4, sticky="ew")
        frame6.grid(column=0, row=5)

        frame2.grid_rowconfigure(tuple(range(self.r)), weight=1)
        frame2.grid_columnconfigure(tuple(range(2)), weight=1)
        self.newWindow.grid_rowconfigure(1, weight=2)
        self.newWindow.grid_columnconfigure(tuple(range(2)), weight=1)

    def getArgs(self, f):
        """ Get required and optional arguments from method.

        Parameters
        ----------
        f : method
                method to extract arguments from

        :returns out: two dictionaries with arguments and default value (if optional)
        """
        
        meth_req = {name: '' for name, param in signature(f).parameters.items() if param.default is param.empty}
        meth_req.pop('self', None)
        meth_r_opt = {name: param.default for name, param in signature(f).parameters.items() if param.default is not param.empty}
        return meth_req, meth_r_opt
    
    def addMeth(self):
        """ Adds selected method in dropdown menu to the plugin tree """
        meth = self.meth2add.get()
        self.meths_sort.append(meth)
        self.tree.insert(parent='', index='end', iid=meth, text='', values=tuple([meth, '']), 
                            tags=('meth',meth))
        # TODO: Remove X and y?
        self.req_settings[meth], self.opt_settings[meth] = self.getArgs(getattr(self.plugin_ini, meth+'_plugin'))
        self.fill_treeview(self.req_settings[meth], self.opt_settings[meth], meth)

    def deleteMeth(self):
        """ Deletes selected method in dropdown menu from the plugin tree """
        meth = self.meth2add.get()
        if meth in self.meths_sort:
            self.meths_sort.remove(meth)
            del self.req_settings[meth]
            del self.opt_settings[meth]
            self.tree.delete(meth)
    
    def moveMeth(self, m):
        meth = self.meth2add.get()
        if meth in self.meths_sort and self.tree.index(meth)+m > 0:
            idx = self.meths_sort.index(meth)
            self.meths_sort.insert(idx+m, self.meths_sort.pop(idx))
            self.tree.move(meth, self.tree.parent(meth), self.tree.index(meth)+m)

    def create_treeView(self, tree_frame, columns_names):
        """ Function to create a new tree view in the given frame

        Parameters
        ----------
        tree_frame : tk.Frame
                    frame where the tree view will be included
        key : str
              key for the tree dictionary
        """

        tree_scrollx = tk.Scrollbar(tree_frame, orient='horizontal')
        tree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        tree_scrolly = tk.Scrollbar(tree_frame)
        tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(tree_frame,
                                yscrollcommand=tree_scrolly.set,
                                xscrollcommand=tree_scrollx.set)
        tree.pack(fill='both', expand=True)

        tree_scrollx.config(command=tree.xview)
        tree_scrolly.config(command=tree.yview)

        tree['columns'] = columns_names

        # Format columns
        tree.column("#0", width=40,
                        minwidth=0, stretch=tk.NO)
        for n, cl in enumerate(columns_names):
            tree.column(
                cl, width=int(self.controller.pages_font.measure(str(cl)))+20,
                minwidth=50, anchor=tk.CENTER)
        # Headings
        for cl in columns_names:
            tree.heading(cl, text=cl, anchor=tk.CENTER)
        tree.tag_configure('req', foreground='black',
                                background='#9fc5e8')
        tree.tag_configure('opt', foreground='black',
                                background='#cfe2f3')
        tree.tag_configure('type', foreground='black',
                                background='#E8E8E8')
        tree.tag_configure('meth', foreground='black',
                                background='#DFDFDF')
        # Define double-click on row action
        tree.bind("<Double-1>", self.OnDoubleClick)
        return tree

    def OnDoubleClick(self, event):
        """ Executed when a row of the treeview is double clicked.
        Opens an entry box to edit a cell. """

        # ii = self.notebook.index(self.notebook.select())
        self.treerow = self.tree.identify_row(event.y)
        self.treecol = self.tree.identify_column(event.x)
        tags = self.tree.item(self.treerow)["tags"]
        if len(tags) > 0 and tags[0] in ['opt', 'req']:
            # get column position info
            x, y, width, height = self.tree.bbox(self.treerow, self.treecol)
            # y-axis offset
            pady = height // 2
            if tags[-1] != 'data':
                if hasattr(self, 'entry'):
                    self.entry.destroy()
                self.entry = tk.Entry(self.tree, justify='center')
                if int(self.treecol[1:]) > 0:
                    value = self.tree.item(self.treerow)['values'][int(str(self.treecol[1:]))-1] 
                    value = str(value) if str(value) not in ['default', 'Choose X or Y'] else ''
                    self.entry.insert(0, value)
                    # self.entry['selectbackground'] = '#123456'
                    self.entry['exportselection'] = False

                    self.entry.focus_force()
                    self.entry.bind("<Return>", self.on_return)
                    self.entry.bind("<Escape>", lambda *ignore: self.entry.destroy())

                    self.entry.place(x=x,
                                    y=y + pady,
                                    anchor=tk.W, width=width)
            else:
                data_list = ['X','Y','X_test','Y_test'] # TODO: Substitute with loaded data
                data_list.insert(0,self.default_inputData['_'.join(tags[:-1])])
                data_list = list(np.unique(data_list))
                self.dropDown = tk.ttk.OptionMenu(self.tree, self.method_inputData['_'.join(tags[:-1])], 
                                             self.method_inputData['_'.join(tags[:-1])].get(), *data_list)
                bg = '#9fc5e8' if tags[0] == 'req' else '#cfe2f3'
                self.dropDown["menu"].configure(bg=bg)
                style = ttk.Style()
                style.configure("new.TMenubutton", background=bg, highlightbackground="black", highlightthickness=1)
                self.dropDown.configure(style="new.TMenubutton")
                self.dropDown.place(x=x,
                                y=y + pady,
                                anchor=tk.W, width=width)

    def on_changeOption(self, *args):
        """ Executed when the optionmenu is selected and pressed enter.
        Saves the value"""
        if hasattr(self, 'dropDown'):
            value = self.tree.item(self.treerow)['values'][int(str(self.treecol[1:]))-2] 
            tags = self.tree.item(self.treerow)["tags"]
            val = self.tree.item(self.treerow)['values']
            new_val = self.method_inputData['_'.join(tags[:-1])].get()
            val[int(self.treecol[1:])-1] = new_val
            self.tree.item(self.treerow, values=tuple([val[0], new_val]))
            self.dropDown.destroy()
            self.saved = False      

    def on_return(self, event):
        """ Executed when the entry is edited and pressed enter.
        Saves the edited value"""

        val = self.tree.item(self.treerow)['values']
        val[int(self.treecol[1:])-1] = self.entry.get()
        if self.entry.get() != '':
            self.tree.item(self.treerow, values=tuple([val[0], self.entry.get()]))
        elif val[1] == '':
            self.tree.item(self.treerow, values=tuple([val[0], 'default']))
        else:
            self.tree.item(self.treerow, values=val)
        self.entry.destroy()
        self.saved = False

    def fill_treeview(self, req_settings, opt_settings, parent = ''):
        """ Adds an entry for each setting. Displays it in the specified row.
        :param req_settings: dict type of plugin required setting options
        :param opt_settings: dict type of plugin optional setting options
        :param parent: string type of parent name
        """
        self.tree.insert(parent=parent, index='end', iid=parent+'_req', text='',
            values=tuple(['Required settings', '']), tags=('type',parent), open=True)
        self.r+=1
        for arg, val in req_settings.items():
            if arg.lower() in ['x', 'y']:
                value = np.array(['X', 'Y'])[arg.lower() == np.array(['x', 'y'])][0]
                self.tree.insert(parent=parent+'_req', index='end', iid=str(self.r), text='',
                    values=tuple([arg, value]), tags=('req',parent,arg,'data'))
                self.method_inputData['req_'+parent+'_'+str(arg)] = tk.StringVar(self.tree)
                self.method_inputData['req_'+parent+'_'+str(arg)].set(value)
                self.method_inputData['req_'+parent+'_'+str(arg)].trace("w", self.on_changeOption)
                self.default_inputData['req_'+parent+'_'+str(arg)] = value
            else:
                self.tree.insert(parent=parent+'_req', index='end', iid=str(self.r), text='',
                                    values=tuple([arg, str(val)]), tags=('req',parent))
            self.r+=1
        self.tree.insert(parent=parent, index='end', iid=parent+'_opt', text='',
            values=tuple(['Optional settings', '']), tags=('type',parent), open=True)
        self.r+=1
        for arg, val in opt_settings.items():
            if arg.lower() in ['x', 'y']:
                self.tree.insert(parent=parent+'_opt', index='end', iid=str(self.r), text='',
                    values=tuple([arg, val]), tags=('opt',parent,arg,'data'))
                self.method_inputData['opt_'+parent+'_'+str(arg)] = tk.StringVar(self.tree)
                self.method_inputData['opt_'+parent+'_'+str(arg)].set(val)
                self.method_inputData['opt_'+parent+'_'+str(arg)].trace("w", self.on_changeOption)
                self.default_inputData['opt_'+parent+'_'+str(arg)] = str(val)
            else:
                self.tree.insert(parent=parent+'_opt', index='end', iid=str(self.r), text='',
                                    values=tuple([arg, str(val)]), tags=('opt',parent))
            self.r+=1

    def removewindow(self):
        """ Stores settings options and closes window """
        # Updates the tree with any unclosed dropDown menu
        if hasattr(self, 'dropDown'):
            for data in self.method_inputData.keys():
                tags = data.split('_')
                el = self.get_element_from_tags(*tags)
                val = self.tree.item(el)['values']
                new_val = self.method_inputData[data].get()
                val[int(self.treecol[1:])-1] = new_val
                self.tree.item(el, values=tuple([val[0], new_val]))
                self.dropDown.destroy()
        # Updates the modified options and removes the ones that are not
        for f in self.tree.get_children():
            for c in self.tree.get_children(f):
                for child in self.tree.get_children(c):
                    tags = self.tree.item(child)["tags"]
                    if tags[0] in ['req', 'opt']:
                        if tags[-1] == 'data':
                            self.updateSettings(tags[0], tags[1], tags[2], self.method_inputData['_'.join(tags[:-1])].get())
                        else:
                            val = self.tree.item(child)["values"]
                            self.settingOptions(tags[0], f, val)
        if hasattr(self, 'model'):
            del self.plugin_ini
        self.newWindow.destroy()
        self.newWindow = None
        self.focus()
    
    def get_all_children(self, item=""):
        """ Iterates over the treeview to get all children """
        children = self.tree.get_children(item)
        for child in children:
            children += self.get_all_children(child)
        return children

    def get_element_from_tags(self, *args):
        """ Finds item in tree with specified tags """
        el = set(self.tree.tag_has(args[0]))
        for arg in args[1:]:
            el = set.intersection(el, set(self.tree.tag_has(arg)))
        return list(el)[0]

    def settingOptions(self, tag, f, val):
        """ Identifies how the data should be stored """
        if val[1] == 'default' or len(str(val[1])) == 0:
            self.updateSettings(tag, f, val[0])
        else:
            self.updateSettings(tag, f, val[0], val[1])

    def updateSettings(self, tag, f, key, value = None):
        """ Return the selected settings 

        Parameters
        ----------
        tag : str
              tag for the settings
        """

        value = self.str_to_bool(value)
        if tag == 'req':
            if value is not None or self.isNotClose(self.req_settings[f][key], value):
                self.req_settings[f][key] = value
            else:
                self.req_settings[f].pop(key, None)
        elif tag == 'opt':
            if self.isNotClose(self.opt_settings[f][key], value):
                self.opt_settings[f][key] = value
            else:
                self.opt_settings[f].pop(key, None)

    def isNotClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        a = self.xml_handler._str_to_num(a) if isinstance(a, (str)) else a
        b = self.xml_handler._str_to_num(b) if isinstance(b, (str)) else b
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(a-b) > max(rel_tol * max(abs(a), abs(b)), abs_tol)
        else:
            return a != b
    
    def str_to_bool(self, s):
        if type(s) is str:
            if s == 'True':
                return True
            elif s == 'False':
                return False
            elif s == 'None':
                return None
            else:
                return s
        else:
            return s
    
    def on_return_entry(self, r):
        """ Changes focus to the next available entry. When no more, focuses 
        on the finish button.
        : param r: int type of entry id.
        """
        if r < len(self.entry):
            self.entry[r].focus()
        else:
            self.finishButton.focus()

    def CreateToolTip(self, widget, text):
        """ Calls ToolTip to create a window with a widget description. """
        toolTip = ToolTip(widget)

        def enter(event):
            toolTip.showtip(text)

        def leave(event):
            toolTip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
        
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

    def add_module(self,boxName: str,x: float,y:float,ini = False,out = False, iid = None):
        """ Creates a rectangular module with the corresponding text inside.

        :param boxName: name of the model
        :type boxName: str
        :param x: float type of module x coordinate
        :param y: float type of module y coordinate
        :param ini: bool type of whether the module corresponds to initialiser.
        :param out: bool type of whether the module corresponds to output.
        """
        iid = self.modules if iid is None else iid
        if ini: #Make initialisation and output unmoveable
            tag = ('n0',)
        elif out:
            tag = ('n1',)
        else:
            tag = ('o'+str(iid),)
        text_w = self.controller.pages_font.measure(boxName+'-00') + 10
        self.canvas.create_rectangle(
            x - text_w/2 , 
            y - self.h/2, 
            x + text_w/2, 
            y + self.h/2, 
            tags = tag + ('p'+str(iid),), 
            fill = self.bg, 
            width = 3,
            # activefill = '#dbaa21'
        )
        self.canvas.create_text(
            x, 
            y, 
            font = self.controller.pages_font, 
            text = boxName, 
            tags = tag + ('t'+str(iid),), 
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
                tags = tag + ('d'+str(iid),))
            
        if not ini:
            self.canvas.create_oval(
                x - self.cr, 
                y - self.h/2 - self.cr, 
                x + self.cr, 
                y - self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('u'+str(iid),))
        
        if not out and not ini:
            self.canvas.create_oval(
                x - text_w/2 - self.cr, 
                y - self.cr, 
                x - text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('l'+str(iid),))
        
            self.canvas.create_oval(
                x + text_w/2 - self.cr, 
                y - self.cr, 
                x + text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('r'+str(iid),))
            
        self.canvas_startxy.append((x, y))
        self.connections[iid] = {}
        self.module_out(boxName, iid)
        self.module_list.append(boxName)
        self.modules += 1

    def upload(self):
        """ Opens the XML file that was previously uploaded and places the 
        modules, loops and connections in the canvas."""

        filename = self.controller.output["xml_filename"]

        self.reset()

        self.xml_handler = XML_handler()
        self.xml_handler.load_XML(filename)
        modules = self.xml_handler.loaded_modules
        modout = modules['Output']
        # They are generated when resetting
        del modules['Initialiser'], modules['Output']
        self.disp_mod = ['Initialiser', 'Output']
        self.id_mod = [0, 1]

        # Place the modules
        self.place_modules(modules)
        self.draw_connection(modules)
        connect = list(modout['coordinates'][2].keys())
        for p, parent in enumerate(modout['parents']):
            parent_id = self.id_mod[np.where(
                np.array(self.disp_mod) == parent)[0][0]]
            out, ins = modout['coordinates'][2][connect[p]].split('-')
            xout, yout, _, _ = self.canvas.coords(out[0]+str(parent_id))
            xins, yins, _, _ = self.canvas.coords(ins[0]+str(1))
            self.canvas.create_line(
                xout + self.cr,
                yout + self.cr,
                xins + self.cr,
                yins + self.cr,
                fill = "red",  width = 2,
                arrow = tk.LAST, arrowshape = (12,10,5), 
                tags=('o'+str(parent_id),
                      'o'+str(1), modout['coordinates'][2][connect[p]]))
            self.out_data.iloc[int(parent_id)].iloc[1] = 1
            self.connections[1][
                int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(1)
        self.m: int = self.id_mod[2]
        x0, y0, x1, y1 = self.canvas.coords('p'+str(self.m))

        # Configure frame for scrollbar
        self.frame_canvas.configure(
            yscrollcommand=self.tree_scrolly.set, xscrollcommand=self.tree_scrollx.set)
        self.frame_canvas.bind('<Configure>', lambda e: self.frame_canvas.configure(
            scrollregion=self.frame_canvas.bbox("all")))
        self.framep = tk.Frame(self.frame_canvas, bg=self.bg)
        self.frame_canvas.create_window((0, 0), window=self.framep)

        self.set_mousewheel(
            self.frame_canvas, lambda e: self.frame_canvas.yview_scroll(-1*(e.delta//120), "units"))

        self.select(x0, y0)

        self.framex.grid(column=1, row=1, sticky="nswe",
                         rowspan=4, pady=(0, 10))
        self.framex.grid_columnconfigure(tuple(range(2)), weight=1)
        self.frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Define modules for output data selection
        for choice in self.module_names:
            var = tk.StringVar(value=choice)
            var.set(0)
            self.out_data_list.append(var)

    def set_mousewheel(self, widget, command):
        """Activate / deactivate mousewheel scrolling when 
        cursor is over / not over the widget respectively."""
        widget.bind("<Enter>", lambda _: widget.bind_all(
            '<MouseWheel>', command))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))
            
    def place_modules(self, modules):
        # Place the modules
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
                                             tag='loop-'+str(l))  # type: ignore
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
                    font=self.controller.pages_font,
                    text=modules[key]['condition'],
                    tags=('loop-'+str(l), 'condition'+'-'+str(l)),
                    justify=tk.CENTER)
                self.loops.append({'type': modules[key]['type'],
                                   'condition': modules[key]['condition'],
                                   'mod': [],
                                   'coord': (x0, y0,
                                             x1, y1)})
                self.place_modules(modules[key])
            elif key not in self.disp_mod:
                # Display module
                self.add_module(key,
                                modules[key]['coordinates'][0][0],
                                modules[key]['coordinates'][0][1], 
                                iid = modules[key]['coordinates'][1])
                self.module_list[-1] = modules[key]['module_type']
                self.id_mod.append(modules[key]['coordinates'][1])
                self.disp_mod.append(key)
        self.module_list = [x for _, x in sorted(zip(self.id_mod, self.module_list))]
        self.canvas_startxy = [x for _, x in sorted(zip(self.id_mod, self.canvas_startxy))]

    def draw_connection(self, modules):
        for key in [key for key, val in modules.items() if type(val) == dict]:
            if modules[key]['class'] == 'loop':
                self.draw_connection(modules[key])
            else:
                # Connect modules
                connect = list(modules[key]['coordinates'][2].keys())
                for p, parent in enumerate(modules[key]['parents']):
                    if not (parent[:4] == 'loop'):
                        # parent_id = modules[parent]['coordinates'][1]
                        parent_id = self.id_mod[np.where(np.array(self.disp_mod) == parent)[0][0]]
                        out, ins = modules[key]['coordinates'][2][connect[p]].split('-')
                        xout, yout, _ , _ = self.canvas.coords(out)
                        xins, yins, _, _ = self.canvas.coords(ins)
                        self.canvas.create_line(
                                    xout + self.cr,
                                    yout + self.cr,
                                    xins + self.cr,
                                    yins + self.cr,
                                    fill = "red",  width = 2,
                                    arrow = tk.LAST, arrowshape = (12,10,5), 
                                    tags = ('o'+str(parent_id),
                                          # 'o'+str(self.id_mod[-1]), 
                                          modules[key]['coordinates'][2][connect[p]]))
                        self.out_data.iloc[int(parent_id)].iloc[int(ins[1:])] = 1
                        self.connections[int(ins[1:])][
                            int(parent_id)] = out[0]+str(out[1:]) + '-' + ins[0]+str(ins[1:])
                    else:
                        self.loops[-1]['mod'].append(key)

    def reset(self):
        """ Resets the canvas and the stored information."""
        self.canvas.delete(tk.ALL)  # Reset canvas

        if hasattr(self, 'newWindow') and (self.newWindow != None):
            self.newWindow.destroy()

        self.canvas_startxy = []
        self.out_data = pd.DataFrame()
        self.connections = {}
        self.modules = 0
        self.module_list = []
        self.module_names = []

        self.add_module('Initialiser', self.width/2, self.h, ini=True)
        self.add_module('Output', self.width/2, self.height - self.h, out=True)

        self.draw = False
        self.loops = []
        self.drawLoop = False
        self.l = 0
        self.id_done = [0]
        self.plugin = {}
        for widget in self.allWeHearIs:
            widget.grid_remove()
        self.allWeHearIs = []
        self.my_label.config(text='')

    def check_quit(self):
        """Checks if all plugins are specified to reset and go back to the startpage"""
        if not len(self.id_done) == len(self.id_mod):
            response = messagebox.askokcancel(
                "Exit",
                "There are some unspecified plugins. Are you sure you want to leave?")
            if response:
                self.reset()
                self.canvas.delete(tk.ALL)
                self.frame_canvas.delete(tk.ALL)
                self.saved = True
                self.xml_handler.write_to_XML()
                self.controller.Plugin.set(True)
                self.controller._show_frame("MainPage")
        # TODO: Check if loaded
        elif not hasattr(self,"xml_handler") or len(self.xml_handler.loaded_modules) == 0:
            self.controller._show_frame("MainPage")
            self.controller.Plugin.set(False)
        else:
            self.reset()
            self.canvas.delete(tk.ALL)
            self.frame_canvas.delete(tk.ALL)
            self.xml_handler.write_to_XML()
            self.controller.Plugin.set(True)
            self.controller._show_frame("MainPage")


class ToolTip(object):
    """ Defines a text window associated to a widget with a description. """

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 60
        y = y + cy + self.widget.winfo_rooty() + 50
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#d0d4d9", relief=tk.SOLID, borderwidth=1,
                         font=("Helvetica", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class EntryWithPlaceholder(tk.Entry):
    """ Defines an entry with a placeholder text displayed if not focused on."""

    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
