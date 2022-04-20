import numpy as np
from importlib import import_module
from .. import Settings

class Core(Settings):
    def __init__(self) -> None:
        super().__init__()

    def load_config_file(self, filename:str):
        self.load_XML(filename)

    def launch_canvas(self):
        from .. import AID
        self.canvas = AID()
        self.canvas.plugin_name("aidcanvas")
        self.canvas.launch()

    def _execute_module(self, specs):
        mod_class = specs["module_type"]
        imp = import_module("..{}".format(mod_class),"aidesign.{0}".format(mod_class))
        mod = getattr(imp,mod_class)()
        mod.launch()


    def run(self):
        for key in self.loaded_modules.keys():
            print (self.loaded_modules[key]["class"])
            if self.loaded_modules[key]["class"] =="module":
                self._execute_module(self.loaded_modules[key])
