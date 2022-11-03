from vai_lab.Data.xml_handler import XML_handler
from vai_lab._plugin_helpers import PluginSpecs
from vai_lab._import_helper import get_lib_parent_dir

import os
import numpy as np
import pandas as pd

from typing import Dict, List
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, ttk


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
        self.s = XML_handler()

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

        self.m: int
        self.w, self.h = 100, 50
        self.cr = 4
        self.canvas.bind('<Button-1>', self.on_click)
        self.id_done = [0, 1]
        self.id_mod:List[int] = [0, 1]
        self.out_data = pd.DataFrame()
        self.plugin: Dict[int, tk.StringVar] = {}
        self.dataType: Dict[int, tk.StringVar] = {}
        self.allWeHearIs: List[tk.Radiobutton] = []

        self.my_label = tk.Label(self.frame2,
                                 text='',
                                 pady=10,
                                 font=self.controller.title_font,
                                 bg=self.bg,
                                 fg='white',
                                 anchor=tk.CENTER)
        self.my_label.grid(column=5,
                           row=0, columnspan=2, padx=10)

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

        tk.Button(
            frame3, text='Load Pipeline', fg='white', bg=parent['bg'],
            height=3, width=15, font=self.controller.pages_font,
            command=self.upload).grid(column=0, row=0, sticky="news",
                                      padx=(10, 0), pady=(0, 10))
        tk.Button(
            frame3, text='Back to main', fg='white', bg=parent['bg'],
            height=3, width=15, font=self.controller.pages_font,
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
        self.frame2.grid(column=1, row=0, sticky="new")
        frame3.grid(column=0, row=5, sticky="nswe")
        self.frame4.grid(column=1, row=5, sticky="sew")

        # self.frame2.grid_columnconfigure(tuple(range(2)), weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        # frame3.grid_columnconfigure(tuple(range(2)), weight=2)
        frame3.grid_columnconfigure(2, weight=2)
        self.frame4.grid_columnconfigure(2, weight=2)

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

        if self.m in self.id_done and self.m > 1:
            self.canvas.itemconfig('p'+str(self.m), fill='#46da63')
        else:
            self.canvas.itemconfig('p'+str(self.m), fill=self.bg)

        if len(self.canvas.gettags(self.canvas_selected)) > 0:
            if not (len(self.canvas.gettags(self.canvas_selected)[0].split('-')) > 1) and\
                    not (self.canvas.gettags(self.canvas_selected)[0].split('-')[0] == 'loop'):
                self.m = int(self.canvas.gettags(self.canvas_selected)[0][1:])
            if self.m > 1:
                if self.m not in self.id_done and self.m > 1:
                    self.canvas.itemconfig('p'+str(self.m), fill='#dbaa21')
                for widget in self.allWeHearIs:
                    widget.grid_remove()

                self.display_buttons()
                module_number = self.id_mod.index(self.m)
                if not hasattr(self, 'button_forw'):
                    if module_number == len(self.id_mod)-1:
                        self.button_forw = tk.Button(
                            self.frame4, text='Finish', bg=self.bg,
                            font=self.controller.pages_font,
                            fg='white', height=3, width=15,
                            command=self.finish, state=tk.NORMAL, image='')
                    else:
                        pCoord = self.canvas.coords(
                            'p'+str(self.id_mod[module_number+1]))
                        self.button_forw = tk.Button(
                            self.frame4, image=self.forw_img, bg=self.bg,
                            command=lambda: self.select(
                                pCoord[0], pCoord[1]), state=tk.NORMAL)
                    self.button_forw.grid(
                        column=1, row=0, sticky="news", pady=(0, 10), padx=(0, 10))
                    if module_number < 3:
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
                    if module_number == len(self.id_mod)-1:
                        self.button_forw.config(text='Finish', bg=self.bg,
                                                font=self.controller.pages_font,
                                                fg='white', height=3, width=15,
                                                command=self.finish, state=tk.NORMAL, image='')
                    else:
                        pCoord = self.canvas.coords(
                            'p'+str(self.id_mod[module_number+1]))
                        self.button_forw.config(image=self.forw_img, bg=self.bg,
                                                command=lambda: self.select(
                                                    pCoord[0], pCoord[1]), text='', state=tk.NORMAL)
                    if module_number < 3:
                        self.button_back.config(image=self.back_img, bg=self.bg,
                                                state=tk.DISABLED, text='')
                    else:
                        mCoord = self.canvas.coords(
                            'p'+str(self.id_mod[module_number-1]))
                        self.button_back.config(image=self.back_img, bg=self.bg,
                                                command=lambda: self.select(
                                                    mCoord[0], mCoord[1]), text='', state=tk.NORMAL)
            else:  # If user clicks on Initialiser or Output
                self.my_label.config(text='')
                for widget in self.allWeHearIs:
                    widget.grid_remove()
                if hasattr(self, 'button_forw'):
                    self.button_back.config(image=self.back_img, bg=self.bg,
                                            state=tk.DISABLED, text='')
                    pCoord = self.canvas.coords('p'+str(self.id_mod[2]))
                    self.button_forw.config(image=self.forw_img, bg=self.bg,
                                            command=lambda: self.select(
                                                pCoord[0], pCoord[1]), text='', state=tk.NORMAL)

    def finish(self):
        """ Calls function check_quit.
        Before that, it checks if the current module plugins have been changed 
        and, if so, updates their information in the XML_handler class.
        """
        self.check_updated()
        self.check_quit()

    def check_updated(self):
        """ Checks if the current plugin exists and 
        stores/updates the plugin options
        """
        if (self.m in self.plugin.keys()) and\
                (self.plugin[self.m].get() != 'None'):  # add
            self.id_done.append(self.m)
            self.s.append_plugin_to_module(self.plugin[self.m].get(),
                                           {**self.req_settings, **
                                               self.opt_settings},
                                           np.array(self.module_names)[
                self.m == np.array(self.id_mod)][0],
                True)

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
        values = np.append(np.unique(type_list[type_list != None]), 'other') if not any(
            type_list == 'other') else np.unique(type_list[type_list != None])
        for i, t in enumerate(values):
            self.framexx.append(tk.Frame(self.framep, bg=self.bg))
            framexx_name = np.append(
                framexx_name, t if t is not None else 'other')
            print(framexx_name)
            framexx_i.append(0)
            label = tk.Label(self.framexx[-1],
                             text=framexx_name[-1].capitalize(),
                             pady=10,
                             font=self.controller.title_font,
                             bg=self.bg,
                             fg='white')
            label.grid(column=0,
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

    def optionsWindow(self):
        """ Function to create a new window displaying the available options 
        of the selected plugin."""

        module = np.array(self.module_list)[self.m == np.array(self.id_mod)][0]
        ps = PluginSpecs()
        self.opt_settings = ps.optional_settings[module][self.plugin[self.m].get(
        )]
        self.req_settings = ps.required_settings[module][self.plugin[self.m].get(
        )]
        if (len(self.opt_settings) != 0) or (len(self.req_settings) != 0):
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
            frame4 = tk.Frame(self.newWindow)

            # Print settings
            tk.Label(frame1,
                     text="Please indicate your desired options for the "+self.plugin[self.m].get()+" plugin.", anchor=tk.N, justify=tk.LEFT).pack(expand=True)

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

            frame2 = tk.Frame(self.newWindow, bg='green')
            self.r = 1
            self.create_treeView(frame2)
            self.fill_treeview(self.req_settings, self.opt_settings)
            frame2.grid(column=0, row=1, sticky="nswe", pady=10, padx=10)
    
            frame2.grid_rowconfigure(tuple(range(self.r)), weight=1)
            frame2.grid_columnconfigure(tuple(range(2)), weight=1)

            self.finishButton = tk.Button(
                frame4, text='Finish', command=self.removewindow)
            self.finishButton.grid(
                column=1, row=0, sticky="es", pady=(0, 10), padx=(0, 10))
            self.finishButton.bind(
                "<Return>", lambda event: self.removewindow())
            self.newWindow.protocol('WM_DELETE_WINDOW', self.removewindow)

            frame1.grid(column=0, row=0, sticky="ew")
            frame4.grid(column=0, row=2, sticky="se")
            self.newWindow.grid_rowconfigure(1, weight=2)
            self.newWindow.grid_columnconfigure(0, weight=1)

    def create_treeView(self, tree_frame):
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

        self.tree = ttk.Treeview(tree_frame,
                                yscrollcommand=tree_scrolly.set,
                                xscrollcommand=tree_scrollx.set)
        self.tree.pack(fill='both', expand=True)

        tree_scrollx.config(command=self.tree.xview)
        tree_scrolly.config(command=self.tree.yview)

        columns_names = ['Name', 'Type', 'Value']
        self.tree['columns'] = columns_names

        # Format columns
        self.tree.column("#0", width=20,
                        minwidth=0, stretch=tk.NO)
        for n, cl in enumerate(columns_names):
            self.tree.column(
                cl, width=int(self.controller.pages_font.measure(str(cl)))+20,
                minwidth=50, anchor=tk.CENTER)
        # Headings
        for cl in columns_names:
            self.tree.heading(cl, text=cl, anchor=tk.CENTER)
        self.tree.tag_configure('req', foreground='black',
                                background='#9fc5e8')
        self.tree.tag_configure('opt', foreground='black',
                                background='#cfe2f3')
        self.tree.tag_configure('type', foreground='black',
                                background='#E8E8E8')
        self.tree.tag_configure('func', foreground='black',
                                background='#DFDFDF')
        # Define double-click on row action
        self.tree.bind("<Double-1>", self.OnDoubleClick)

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
            # pady = 0

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
    
    def on_return(self, event):
        """ Executed when the entry is edited and pressed enter.
        Saves the edited value"""

        val = self.tree.item(self.treerow)['values']
        val[int(self.treecol[1:])-1] = self.entry.get()
        if self.entry.get() != '':
            self.tree.item(self.treerow, values=tuple([val[0], val[1], self.entry.get()]))
        elif val[2] == '':
            self.tree.item(self.treerow, values=tuple([val[0], val[1], 'default']))
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
            values=tuple(['Required settings', '', '']), tags=('type',))
        self.r+=1
        for arg, val in req_settings.items():
            if arg == 'Data':
                self.tree.insert(parent=parent+'_req', index='end', iid=str(self.r), text='',
                    values=tuple([arg, val, 'Choose X or Y']), tags=('req',))
            else:
                self.tree.insert(parent=parent+'_req', index='end', iid=str(self.r), text='',
                                    values=tuple([arg, val, '']), tags=('req',))
            self.r+=1
        self.tree.insert(parent=parent, index='end', iid=parent+'_opt', text='',
            values=tuple(['Optional settings', '', '']), tags=('type',))
        self.r+=1
        for arg, val in opt_settings.items():
            self.tree.insert(parent=parent+'_opt', index='end', iid=str(self.r), text='',
                                 values=tuple([arg, val, 'default']), tags=('opt',))
            self.r+=1

    def removewindow(self):
        """ Stores settings options and closes window """
        self.req_settings.pop("Data", None)
        children = self.get_all_children()
        for child in children:
            tag = self.tree.item(child)["tags"][0]            
            if tag in ['req', 'opt']:
                val = self.tree.item(child)["values"]
                self.settingOptions(tag, val) 
        self.newWindow.destroy()
        self.newWindow = None
        self.focus()
    
    def get_all_children(self, item=""):
        """ Iterates over the treeview to get all childer """
        children = self.tree.get_children(item)
        for child in children:
            children += self.get_all_children(child)
        return children

    def settingOptions(self, tag, val):
        """ Identifies how the data should be stored """
        if val[0] == 'Data':
            if val[2] == 'Choose X or Y' or len(val[2]) == 0:
                self.updateSettings(tag, val[0], 'X')
            else:
                self.updateSettings(tag, val[0], val[2])
        else:
            if val[2] == 'default' or len(str(val[2])) == 0:
                self.updateSettings(tag, val[0])
            else:
                self.updateSettings(tag, val[0], val[2])

    def updateSettings(self, tag, key, value = None):
        """ Return the selected settings 

        Parameters
        ----------
        tag : str
              tag for the settings
        """
        if tag == 'req':
            if value is not None or self.req_settings[key] != value:
                self.req_settings[key] = value
            else:
                self.req_settings.pop(key, None)
        elif tag == 'opt':
            if value is not None or self.opt_settings[key] != value:
                self.opt_settings[key] = value
            else:
                self.opt_settings.pop(key, None)

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

        self.s = XML_handler()
        self.s.load_XML(filename)
        # self.s._print_pretty(self.s.loaded_modules)
        modules = self.s.loaded_modules
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
                fill="red", width = 2,
                arrow = tk.LAST, arrowshape = (12,10,5),
                tags=('o'+str(parent_id),
                      'o'+str(1), modout['coordinates'][2][connect[p]]))
            self.out_data.iloc[int(parent_id)][1] = 1
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
                                    fill = "red", width = 2,
                                    arrow = tk.LAST, arrowshape = (12,10,5),
                                    tags = ('o'+str(parent_id),
                                          # 'o'+str(self.id_mod[-1]), 
                                          modules[key]['coordinates'][2][connect[p]]))
                        self.out_data.iloc[int(parent_id)][int(ins[1:])] = 1
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
        self.id_done = [0, 1]
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
                self.s.write_to_XML()
                self.controller.Plugin.set(True)
                self.controller._show_frame("MainPage")
        # TODO: Check if loaded
        elif len(self.s.loaded_modules) == 0:
            self.controller._show_frame("MainPage")
            self.controller.Plugin.set(False)
        else:
            self.reset()
            self.canvas.delete(tk.ALL)
            self.frame_canvas.delete(tk.ALL)
            self.s.write_to_XML()
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
