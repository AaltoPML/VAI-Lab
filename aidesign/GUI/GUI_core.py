# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter.font import Font
from aidesign.utils.import_helper import import_plugin_absolute
from aidesign.utils.plugin_helpers import PluginSpecs

class GUI(tk.Tk):
    """
    TODO: This structure still needs serious overhaul. 

    TODO: By having the TKinter controller as in the main GUI module, we are locked to using TKinter which defeats the purpose of being modular. This class needs to only be calling the plugins themselves, not acting as a controller.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_font = Font(family='Helvetica',
                                      size=14,
                                      weight="bold")
        self.pages_font = Font(family='Helvetica',
                                      size=12)

        self._desired_ui_types = []
        self._top_ui_layer = None
        self._module_config = None
        self.closed = False
        self.output = {}
        self._plugin_specs = PluginSpecs()

    def _compare_layer_priority(self, ui_specs):
        """Check if a new module should have higher layer priority than the existing one

        :param ui_name: name of the UI method being compared
        :type ui_name: str
        """
        if self._top_ui_layer == None:
            self._top_ui_layer = ui_specs
        else:
            current_top_layer = self._top_ui_layer["_PLUGIN_MODULE_OPTIONS"]["layer_priority"]
            candidate_layer = ui_specs["_PLUGIN_MODULE_OPTIONS"]["layer_priority"]
            self._top_ui_layer = candidate_layer \
                if candidate_layer < current_top_layer \
                else self._top_ui_layer

    def _add_UI_type_to_frames(self, ui_specs):
        """Add user defined UI method to list of frames to be loaded

        :param ui_name: name of the UI method being loaded
        :type ui_name: str 
        """
        plugin = import_plugin_absolute(globals(),
                                        ui_specs["_PLUGIN_PACKAGE"],
                                        ui_specs["_PLUGIN_CLASS_NAME"])

        self._desired_ui_types.append(plugin)
        self._compare_layer_priority(ui_specs)
        if ui_specs["_PLUGIN_MODULE_OPTIONS"]["required_children"] != None:
            for children in ui_specs["_PLUGIN_MODULE_OPTIONS"]["required_children"]:
                self.set_plugin_name(children)

    def set_plugin_name(self, ui_type: list):
        """"Given user input, create a list of classes of the corresponding User Interface Type 

        :param ui_name: name of the desired User Interface Method
        :type ui_name: str or list
        """
        ui_type = ui_type\
            if isinstance(ui_type, list)\
            else [ui_type]

        for ui in ui_type:
            ui_specs = self._plugin_specs.find_from_readable_name(ui)
            try:
                self._add_UI_type_to_frames(ui_specs)
            except:
                from sys import exit
                print(
                    "Error: User Interface \"{0}\" not recognised. \
                    \nAvailable methods are: \
                    \n  - {1}"\
                    .format(ui, ",\n  - ".join(
                        [i for i in self._plugin_specs.available_plugin_names])))
                exit(1)

    def _append_to_output(self, key:str, value:any):
        self.output[key] = value

    def set_options(self, module_config: dict):
        """Send configuration arguments to GUI

        :param module_config: dict of settings to congfigure the plugin
        """
        self._module_config = module_config
        self.set_plugin_name(self._module_config["plugin"]["plugin_name"])

    def _show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if isinstance(page_name,dict):
            page_name = page_name["_PLUGIN_CLASS_NAME"]
        frame = self.frames[page_name]
        frame.tkraise()

    def _on_closing(self):
        self.closed = True
        self.destroy()
        
    def launch(self):
        """Runs UserInterface Plugin. 
        If multiple frames exist, they are stacked
        """
        container = tk.Frame(self, bg='#064663')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in self._desired_ui_types:
            page_name = F.__name__
            frame = F(parent=container, controller=self,
                      config=self._module_config)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self._show_frame(self._top_ui_layer)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.mainloop()
        return self.output
