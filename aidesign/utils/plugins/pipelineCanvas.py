# Import the required libraries
import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
from tkinter import messagebox

from aidesign.Data.xml_handler import XML_handler
from aidesign._plugin_helpers import PluginSpecs

_PLUGIN_READABLE_NAMES = {"pipeline_canvas": "default",
                          "pipelineCanvas": "alias",
                          "pipeline canvas": "alias"}       # type:ignore
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,              # type:ignore
                          "required_children": None}        # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                              # type:ignore


class pipelineCanvas(tk.Frame):
    """Canvas for the visualisation of the pipeline state."""

    def __init__(self, parent, controller, config: dict):
        """ Here we define the frame displayed for the plugin specification."""

        super().__init__(parent, bg=parent['bg'])
        self.bg = parent['bg']
        self.controller = controller
        self.s = XML_handler()

        script_dir = os.path.dirname(__file__)
        self.tk.call('wm', 'iconphoto', self.controller._w, ImageTk.PhotoImage(
            file=os.path.join(os.path.join(
                script_dir,
                'resources',
                'Assets',
                'AIDIcon.ico'))))
        self.grid_rowconfigure(tuple(range(2)), weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(self, bg=self.bg)
        self.frame2 = tk.Frame(self, bg=self.bg)
        frame3 = tk.Frame(self, bg=self.bg)
        self.frame4 = tk.Frame(self, bg=self.bg)

        # Create canvas
        self.width, self.height = 600, 600
        self.canvas = tk.Canvas(frame1, width=self.width,
                                height=self.height, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

        self.w, self.h = 100, 50
        self.cr = 4
        """
        TODO: Implement clicking on canvas actions
        """
        # self.canvas.bind('<Button-1>', self.on_click)
        self.plugin = {}
        self.allWeHearIs = []

        self.upload()

        self.save_path = ''
        self.saved = True
        frame1.grid(column=0, row=0, sticky="nsew")
        self.frame2.grid(column=1, row=0, sticky="ne")
        frame3.grid(column=0, row=1, sticky="swe")
        self.frame4.grid(column=1, row=1, sticky="sew")

        frame3.grid_columnconfigure(tuple(range(2)), weight=1)
        self.frame4.grid_columnconfigure(tuple(range(2)), weight=1)

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
        if self.selected:
            if len(self.selected) > 2:
                self.canvas.selected = self.selected[-2]
            else:
                self.canvas.selected = self.selected[-1]

        if (self.m in self.plugin.keys()) and\
                (self.plugin[self.m].get() != 'None') and \
                (self.m not in self.id_done):  # add
            self.id_done.append(self.m)
            print(np.array(self.module_names)[
                  self.m == np.array(self.id_mod)][0])
            self.s.append_plugin_to_module(self.plugin[self.m].get(),
                                           {**self.req_settings, **
                                               self.opt_settings},
                                           np.array(self.module_names)[
                self.m == np.array(self.id_mod)][0],
                True)
        if self.m in self.id_done and self.m > 1:
            self.canvas.itemconfig('p'+str(self.m), fill='#46da63')
        else:
            self.canvas.itemconfig('p'+str(self.m), fill=self.bg)

        if len(self.canvas.gettags(self.canvas.selected)) > 0:
            if not (len(self.canvas.gettags(self.canvas.selected)[0].split('-')) > 1) and\
                    not (self.canvas.gettags(self.canvas.selected)[0].split('-')[0] == 'loop'):
                self.m = int(self.canvas.gettags(self.canvas.selected)[0][1:])
            if self.m > 1:
                if self.m not in self.id_done and self.m > 1:
                    self.canvas.itemconfig('p'+str(self.m), fill='#dbaa21')
                for widget in self.allWeHearIs:
                    widget.grid_remove()

            #     self.display_buttons()
            #     module_number = self.id_mod.index(self.m)
            #     if hasattr(self, 'button_forw'):
            #         if module_number == len(self.id_mod)-1:
            #             self.button_forw.config(text = 'Finish', bg = self.bg,
            #                 font = self.controller.pages_font,
            #                 fg = 'white', height = 3, width = 15,
            #                 command = self.finnish, state = tk.NORMAL, image = '')
            #         else:
            #             pCoord = self.canvas.coords('p'+str(self.id_mod[module_number+1]))
            #             self.button_forw.config(image = self.forw_img, bg = self.bg,
            #                 command = lambda: self.select(
            #                     pCoord[0], pCoord[1]), text = '', state = tk.NORMAL)
            #         if module_number < 3:
            #             self.button_back.config(image = self.back_img, bg = self.bg,
            #                 state = tk.DISABLED, text = '')
            #         else:
            #             mCoord = self.canvas.coords('p'+str(self.id_mod[module_number-1]))
            #             self.button_back.config(image = self.back_img, bg = self.bg,
            #                 command = lambda: self.select(
            #                     mCoord[0], mCoord[1]), text = '', state = tk.NORMAL)
            #     else:
            #         if module_number == len(self.id_mod)-1:
            #             self.button_forw = tk.Button(
            #                 self.frame4, text = 'Finish', bg = self.bg,
            #                 font = self.controller.pages_font,
            #                 fg = 'white', height = 3, width = 15,
            #                 command = self.finnish, state = tk.NORMAL, image = '')
            #         else:
            #             pCoord = self.canvas.coords('p'+str(self.id_mod[module_number+1]))
            #             self.button_forw = tk.Button(
            #                 self.frame4, image = self.forw_img, bg = self.bg,
            #                 command = lambda: self.select(
            #                     pCoord[0], pCoord[1]), state = tk.NORMAL)
            #         self.button_forw.grid(column = 1,row = 0, sticky="news", pady=(0,10), padx=(0,10))
            #         if module_number < 3:
            #             self.button_back = tk.Button(
            #                 self.frame4, image = self.back_img, bg = self.bg,
            #                 state = tk.DISABLED)
            #         else:
            #             mCoord = self.canvas.coords('p'+str(self.id_mod[module_number-1]))
            #             self.button_back = tk.Button(
            #                 self.frame4, image = self.back_img, bg = self.bg,
            #                 command = lambda: self.select(
            #                     mCoord[0], mCoord[1]), state = tk.NORMAL)
            #         self.button_back.grid(column = 0,row = 0, sticky="news", pady=(0,10))
            # else: # If user clicks on Initialiser or Output
            #     # self.my_label.config(text = '')
            #     for widget in self.allWeHearIs:
            #         widget.grid_remove()
            #     if hasattr(self, 'button_forw'):
            #         self.button_back.config(image = self.back_img, bg = self.bg,
            #                 state = tk.DISABLED, text = '')
            #         pCoord = self.canvas.coords('p'+str(self.id_mod[2]))
            #         self.button_forw.config(image = self.forw_img, bg = self.bg,
            #                 command = lambda: self.select(
            #                     pCoord[0], pCoord[1]), text = '', state = tk.NORMAL)

    def finnish(self):
        """ Calls function check_quit.
        Before that, it checks if the current module plugins have been changed 
        and, if so, updates their information in the XML_handler class.
        """
        if (self.m in self.plugin.keys()) and\
                (self.plugin[self.m].get() != 'None') and \
                (self.m not in self.id_done):  # add
            self.id_done.append(self.m)
            self.s.append_plugin_to_module(self.plugin[self.m].get(),
                                           {**self.req_settings, **
                                               self.opt_settings},
                                           np.array(self.module_names)[
                self.m == np.array(self.id_mod)][0],
                True)
        self.check_quit()

    def display_buttons(self):
        """ Updates the displayed radiobuttons and the description windows.
        It loads the information corresponding to the selected module (self.m)
        and shows the available plugins and their corresponding descriptions.
        """
        module = np.array(self.module_list)[self.m == np.array(self.id_mod)][0]
        name = self.canvas.itemcget('t'+str(self.m), 'text')
        # self.my_label.config(text = 'Choose a plugin for the '+name+' module')
        ps = PluginSpecs()
        plugin_list = list(ps.class_names[module].values())
        plugin_list.append('Custom')
        descriptions = list(ps.class_descriptions[module].values())
        descriptions.append('User specified plugin')
        if self.m not in self.plugin:
            self.plugin[self.m] = tk.StringVar()
            self.plugin[self.m].set(None)
        self.allWeHearIs = []
        for p, plug in enumerate(plugin_list):
            rb = tk.Radiobutton(self.frame2, text=plug, fg='white', bg=self.bg,
                                height=3, width=20, var=self.plugin[self.m],
                                selectcolor='black', value=plug,
                                font=self.controller.pages_font, command=self.optionsWindow)
            rb.grid(column=5 + (p % 2 != 0), row=int(p/2)+1)
            self.CreateToolTip(rb, text=descriptions[p])
            self.allWeHearIs.append(rb)

    def optionsWindow(self):
        """ Function to create a new window displaying the available options 
        of the selected plugin."""

        module = np.array(self.module_list)[self.m == np.array(self.id_mod)][0]
        ps = PluginSpecs()
        self.opt_settings = ps.optional_settings[module][self.plugin[self.m].get(
        ).lower()+'.py']
        self.req_settings = ps.required_settings[module][self.plugin[self.m].get(
        ).lower()+'.py']
        # req_settings = {'arg1': 'int', 'arg2': ['C', 'F']}
        # opt_settings = {'arg3': 'int', 'arg4': ['C', 'F']}
        if (len(self.opt_settings) != 0) or (len(self.req_settings) != 0):
            if hasattr(self, 'newWindow') and (self.newWindow != None):
                self.newWindow.destroy()
            self.newWindow = tk.Toplevel(self.controller)
            # Window options
            self.newWindow.title(self.plugin[self.m].get()+' plugin options')
            script_dir = os.path.dirname(__file__)
            self.tk.call('wm', 'iconphoto', self.newWindow, ImageTk.PhotoImage(
                file=os.path.join(os.path.join(
                    script_dir,
                    'resources',
                    'Assets',
                    'AIDIcon.ico'))))
            self.newWindow.geometry("350x400")

            frame1 = tk.Frame(self.newWindow)
            frame4 = tk.Frame(self.newWindow)

            # Print settings
            tk.Label(frame1,
                     text="Please indicate your desired options for the "+self.plugin[self.m].get()+" plugin.", anchor=tk.N, justify=tk.LEFT).pack(expand=True)
            self.entry = []
            # Required
            r = 1
            if len(self.req_settings) > 0:
                frame2 = tk.Frame(self.newWindow)
                tk.Label(frame2,
                         text="Required settings:", anchor=tk.W, justify=tk.LEFT).grid(row=0, column=0, columnspan=2)
                self.displaySettings(frame2, self.req_settings)
                frame2.grid(column=0, row=r, sticky="nswe")
                r += 1
            # Optional
            if len(self.opt_settings) > 0:
                frame3 = tk.Frame(self.newWindow)
                tk.Label(frame3,
                         text="Optional settings:", anchor=tk.W, justify=tk.LEFT).grid(row=0, column=0, columnspan=2)
                self.displaySettings(frame3, self.opt_settings)
                frame3.grid(column=0, row=r, sticky="nswe")
                r += 1

            self.entry[0].focus()
            self.finishButton = tk.Button(
                frame4, text='Finish', command=self.removewindow)
            self.finishButton.grid(
                column=1, row=r+1, sticky="es", pady=(0, 10), padx=(0, 10))
            self.finishButton.bind(
                "<Return>", lambda event: self.removewindow())
            self.newWindow.protocol('WM_DELETE_WINDOW', self.removewindow)

            frame1.grid(column=0, row=0, sticky="new")
            frame4.grid(column=0, row=r, sticky="se")
            self.newWindow.grid_rowconfigure(0, weight=1)
            self.newWindow.grid_rowconfigure(tuple(range(r+1)), weight=2)
            self.newWindow.grid_columnconfigure(0, weight=1)

    def displaySettings(self, frame, settings):
        """ Adds an entry for each input setting. Displays it in the specified row.
        :param frame: tkinter frame type of frame
        :param settings: dict type of plugin setting options
        """
        r = 1
        for arg, val in settings.items():
            tk.Label(frame,
                     text=arg).grid(row=r, column=0)
            self.entry.append(EntryWithPlaceholder(frame, val))
            self.entry[-1].grid(row=r, column=1)
            self.entry[-1].bind("<Return>", lambda event,
                                a=len(self.entry): self.on_return_entry(a))
            r += 1
        frame.grid_rowconfigure(tuple(range(r)), weight=1)
        frame.grid_columnconfigure(tuple(range(2)), weight=1)

    def removewindow(self):
        """ Stores settings options and closes window """
        for e, ent in enumerate(self.entry):
            if e < len(self.req_settings):
                self.req_settings[list(self.req_settings.keys())[
                    e]] = ent.get()
            else:
                print(self.opt_settings)
                print(list(self.opt_settings.keys()))
                print(e-len(self.req_settings))
                self.opt_settings[list(self.opt_settings.keys())[
                    e-len(self.req_settings)]] = ent.get()
        self.newWindow.destroy()
        self.newWindow = None
        self.focus()

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
        self.canvas.itemconfig('t'+str(self.modules), text=name_list[-1])
        values = self.out_data.values
        values = np.vstack((
            np.hstack((values, np.zeros((values.shape[0], 1)))),
            np.zeros((1, values.shape[0]+1))))
        self.out_data = pd.DataFrame(values,
                                     columns=name_list,
                                     index=name_list)
        self.module_names.append(name_list[-1])

    def add_module(self, boxName: str, x: float, y: float, ini=False, out=False):
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
        else:  # Make initialisation and output unmoveable
            tag = ('n0',)
        text_w = self.controller.pages_font.measure(boxName+'-00') + 10
        self.canvas.create_rectangle(
            x - text_w/2,
            y - self.h/2,
            x + text_w/2,
            y + self.h/2,
            tags=tag + ('p'+str(self.modules),),
            fill=self.bg,
            width=3,
            # activefill = '#dbaa21'
        )
        self.canvas.create_text(
            x,
            y,
            font=self.controller.pages_font,
            text=boxName,
            tags=tag + ('t'+str(self.modules),),
            fill='#d0d4d9',
            justify=tk.CENTER)

        if not out:
            self.canvas.create_oval(
                x - self.cr,
                y + self.h/2 - self.cr,
                x + self.cr,
                y + self.h/2 + self.cr,
                width=2,
                fill='black',
                tags=tag + ('d'+str(self.modules),))

        if not ini:
            self.canvas.create_oval(
                x - self.cr,
                y - self.h/2 - self.cr,
                x + self.cr,
                y - self.h/2 + self.cr,
                width=2,
                fill='black',
                tags=tag + ('u'+str(self.modules),))

        if not out and not ini:
            self.canvas.create_oval(
                x - text_w/2 - self.cr,
                y - self.cr,
                x - text_w/2 + self.cr,
                y + self.cr,
                width=2,
                fill='black',
                tags=tag + ('l'+str(self.modules),))

            self.canvas.create_oval(
                x + text_w/2 - self.cr,
                y - self.cr,
                x + text_w/2 + self.cr,
                y + self.cr,
                width=2,
                fill='black',
                tags=tag + ('r'+str(self.modules),))

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
        self.s._print_pretty(self.s.loaded_modules)
        modules = self.s.loaded_modules
        modout = modules['output']
        # They are generated when resetting
        del modules['Initialiser'], modules['output']
        self.disp_mod = ['Initialiser', 'output']
        self.id_mod = [0, 1]

        # Place the modules
        self.place_modules(modules)
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
                fill="red",
                arrow=tk.LAST,
                tags=('o'+str(parent_id),
                      'o'+str(1), modout['coordinates'][2][connect[p]]))
            self.out_data.iloc[int(parent_id)][1] = 1
            self.connections[1][
                int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(1)
        self.m = self.id_mod[2]
        x0, y0, x1, y1 = self.canvas.coords('p'+str(self.m))
        self.select(x0, y0)

    def place_modules(self, modules: dict):
        """Places the modules in the dictionary in the canvas.
        :param modules: dict type of modules in the pipeline.
        """

        for key in [key for key, val in modules.items() if type(val) == dict]:
            if modules[key]['class'] == 'loop':
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
                        parent_id = self.id_mod[np.where(
                            np.array(self.disp_mod) == parent)[0][0]]
                        out, ins = modules[key]['coordinates'][2][connect[p]].split(
                            '-')
                        xout, yout, _, _ = self.canvas.coords(
                            out[0]+str(parent_id))
                        xins, yins, _, _ = self.canvas.coords(
                            ins[0]+str(self.id_mod[-1]))
                        self.canvas.create_line(
                            xout + self.cr,
                            yout + self.cr,
                            xins + self.cr,
                            yins + self.cr,
                            fill="red",
                            arrow=tk.LAST,
                            tags=('o'+str(parent_id),
                                  'o'+str(self.id_mod[-1]), modules[key]['coordinates'][2][connect[p]]))
                        self.out_data.iloc[int(parent_id)][int(
                            self.id_mod[-1])] = 1
                        self.connections[int(self.id_mod[-1])][
                            int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(self.id_mod[-1])
                    else:
                        self.loops[-1]['mod'].append(key)
                self.disp_mod.append(key)

    def reset(self):
        """ Resets the canvas and the stored information."""
        self.canvas.delete(tk.ALL)  # Reset canvas

        if hasattr(self, 'newWindow') and (self.newWindow != None):
            self.newWindow.destroy()

        self.canvas.startxy = []
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
        # self.my_label.config(text = '')

    def check_quit(self):
        """Checks if all plugins are specified to reset and go back to the startpage"""
        if not len(self.id_done) == len(self.id_mod):
            response = messagebox.askokcancel(
                "Exit",
                "There are some unspecified plugins. Are you sure you want to leave?")
            if response:
                self.reset()
                self.canvas.delete(tk.ALL)
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


if __name__ == "__main__":
    app = pluginCanvas()
    app.mainloop()
