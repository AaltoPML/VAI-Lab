import tkinter as tk
from tkinter import font  as tkfont
from aidesign.utils.import_helper import import_plugin

from aidesign.GUI.GUI_core import GUI
class UserFeedback(GUI):
    """UserFeedback core class directly uses GUI_core.py"""
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica',
                                      size=14,
                                      weight="bold")
        self.pages_font = tkfont.nametofont("TkDefaultFont")

        self.desired_ui_types = []
        self.top_ui_layer = None
        # self.startpage_exist = False
        self.available_ui_types = {
            "ManualInput": {
                "name": "manual",
                "layer_priority": 2,
                "required_children": None,
            },
            "CanvasInput": {
                "name": "canvas",
                "layer_priority": 2,
                "required_children": None,
            }
        }

    def _compare_layer_priority(self, ui_name):
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

    def _add_UI_type_to_frames(self, ui_name):
        """Add user defined UI method to list of frames to be loaded

        :param ui_name: name of the UI method being loaded
        :type ui_name: str 
        """
        try:
            plugin = import_plugin(globals(),ui_name)
        except:
            from sys import exit
            print(
                "Error: User Interface \"{0}\" not recognised. \
                \nAvailable methods are: \
                \n  - {1}"\
                .format(ui_name, ",\n  - ".join(
                    [i["name"]for i in self.available_ui_types.values()])))
            exit(1)
        self.desired_ui_types.append(plugin)
        self._compare_layer_priority(ui_name)
        if self.available_ui_types[ui_name]["required_children"] != None:
            for children in self.available_ui_types[ui_name]["required_children"]:
                self._add_UI_type_to_frames(children)

    def _set_plugin_name(self, ui_type: list):
        """"Given user input, create a list of classes of the corresponding User Interface Type 

        :param ui_name: name of the desired User Interface Method
        :type ui_name: str or list
        """
        ui_type = ui_type\
            if isinstance(ui_type, list)\
            else [ui_type]
        for ui in ui_type:
            print(ui)
            # ui_name = ''.join(kn for kn in self.available_ui_types.keys()
            #                   if ui.lower() == self.available_ui_types[kn]["name"])
            ui_name = ''.join(kn for kn in self.available_ui_types.keys()
                              if self.available_ui_types[kn]["name"] in ui.lower())
            print(ui_name)
            self._add_UI_type_to_frames(ui_name)


    def _show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def set_options(self, module_config: dict):
        """Send configuration arguments to GUI

        :param module_config: dict of settings to congfigure the plugin
        """
        self.module_config = module_config
        self._set_plugin_name(self.module_config["plugin"]["plugin_name"])


    def launch(self):
        """Runs UserInterface Plugin. 
        If multiple frames exist, they are stacked
        """
        container = tk.Frame(self, bg='#064663')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in self.desired_ui_types:
            page_name = F.__name__
            frame = F(parent=container, controller=self,
                      config=self.module_config)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self._show_frame(self.top_ui_layer)
        self.mainloop()
