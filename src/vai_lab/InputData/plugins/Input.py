from vai_lab._plugin_templates import InputDataPluginT

from vai_lab.Data.Data_core import Data as model
import pandas as pd

_PLUGIN_READABLE_NAMES = {"Input": "default",
                          "input": "alias"}                         # type:ignore
_PLUGIN_MODULE_OPTIONS = {}                                         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                      # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                          # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X", "Y", "X_tst", 'Y_tst'}                # type:ignore

class Input(InputDataPluginT):
    """
    Import data to the pipeline or append column to existing data
    """

    def __init__(self, config = {}, data_in = [None], ini = False):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        if not ini:
            # Model configuration
            self.set_data_in(data_in)
            self.configure(config)
            # Model initialisation    
            try:    
                self.model = model(**self._config["options"])
            except Exception as exc:
                print('The plugin encountered an error on the parameters of '
                        +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
                raise
        else:
            self.model = model
            
        self.import_plugin = self.model.import_data
        self.append_plugin = self.model.append_data_column