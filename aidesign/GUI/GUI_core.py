# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font as tkfont
from sys import modules as get_module_name
from .plugins import PageCanvas
from .plugins import PageManual
from .plugins import StartPage


class GUI(tk.Tk):
    """
    TODO: This structure still needs serious overhaul. 

    TODO: By having the TKinter controller as in the main GUI module, we are locked to using TKinter which defeats the purpose of being modular. This class needs to only be calling the plugins themselves, not acting as a controller.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica',
                                      size=14,
                                      weight="bold")
        self.pages_font = tkfont.nametofont("TkDefaultFont")
        self.current_module_name = get_module_name[__name__]

        self.desired_ui_types = []
        self.top_ui_layer = None
        self.startpage_exist = False
        self.available_ui_types = {
            "StartPage": {
                "name": "startpage",
                "layer_priority": 1,
                "required_children": ["PageManual", "PageCanvas"]
            },
            "PageManual": {
                "name": "manual",
                "layer_priority": 2,
                "required_children": None,
                # temporary fix so startpage still works:
                "default_class_list": ['Atelectasis',
                                       'Cardiomelagy',
                                       'Effusion',
                                       'Infiltration',
                                       'Mass',
                                       'Nodule',
                                       'Pneumonia',
                                       'Pneumothorax'
                                       ]
            },
            "PageCanvas": {
                "name": "canvas",
                "layer_priority": 2,
                "required_children": None,
                # temporary fix so startpage still works:
                "default_class_list": [['State_a', 'Action_a'],
                                       ['State_x', 'State_y',
                                        'Action_x', 'Action_y'],
                                       ['State_x', 'State_y', 'Action_x', 'Action_y']]
            }
        }

    def compare_layer_priority(self, ui_name):
        """Check if a new module should have higher layer priority than the existing one

        :param ui_name: name of the UI method being compared
        :type ui_name: str
        """
        if self.top_ui_layer == None:
            self.top_ui_layer = ui_name
        else:
            current_top_layer = self.available_ui_types[self.top_ui_layer]["layer_priority"]
            candidate_layer = self.available_ui_types[ui_name]["layer_priority"]
            self.top_ui_layer = candidate_layer \
                if candidate_layer < current_top_layer \
                else self.top_ui_layer

    def add_UI_type_to_frames(self, ui_name):
        """Add user defined UI method to list of frames to be loaded

        :param ui_name: name of the UI method being loaded
        :type ui_name: str 
        """
        self.desired_ui_types.append(
            getattr(self.current_module_name, ui_name))
        self.compare_layer_priority(ui_name)
        if self.available_ui_types[ui_name]["required_children"] != None:
            for children in self.available_ui_types[ui_name]["required_children"]:
                self.add_UI_type_to_frames(children)

    def plugin_name(self, ui_type):
        """"Given user input, create a list of classes of the corresponding User Interface Type 

        :param ui_name: name of the desired User Interface Method
        :type ui_name: str or list
        """
        ui_type = ui_type\
            if isinstance(ui_type, list)\
            else [ui_type]  # put ui_type in list if not already

        for ui in ui_type:
            ui_name = ''.join(kn for kn in self.available_ui_types.keys()
                              if ui.lower() == self.available_ui_types[kn]["name"])
            try:
                self.add_UI_type_to_frames(ui_name)
                self.startpage_exist = 1 if ui_name == "StartPage" else self.startpage_exist
            except:
                from sys import exit
                print(
                    "Error: User Interface \"{0}\" not recognised.".format(ui))
                print("Available methods are:")
                print(
                    "   - {}".format(",\n   - ".join([i["name"] for i in self.available_ui_types.values()])))
                exit(1)

    def set_options(self, specs):
        self.plugin_name(specs["plugin"]["plugin_name"])
        self.set_class_list(specs["plugin"]["options"]["class_list"])

    def set_class_list(self, class_list):
        self._class_list = class_list

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def launch(self):
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg='#19232d')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in self.desired_ui_types:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            if not self.startpage_exist:
                frame.class_list(self._class_list)
            elif self.startpage_exist and page_name != "StartPage":
                default_class_list = self.available_ui_types[page_name]["default_class_list"]
                frame.class_list(default_class_list)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.top_ui_layer)
        self.mainloop()
