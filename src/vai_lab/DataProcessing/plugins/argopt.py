from distutils.command.config import config
from numpy import argmin, argmax
from vai_lab._plugin_templates import DataProcessingT
import pandas as pd

_PLUGIN_READABLE_NAMES = {"argopt": "default",
                          "argmax": "alias",            
                          "argmin": "alias"}            # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "math operator"}      # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}             # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {'min/max': "str"}          # type:ignore
_PLUGIN_REQUIRED_DATA = {}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}      # type:ignore

class argopt(DataProcessingT):
    """
    Calculate the optimum argument
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        # self.proc = model()

    def configure(self, config: dict):
        """Sets and parses plugin configurations options
        :param config: dict of internal tags set in the XML config file 
        """
        # super().configure(config)
        self.config = config

    def set_data_in(self, data_in):
        """Sets and parses incoming data
        :param data_in: saves data as class variable
                        expected type: aidesign.Data.Data_core.Data
        """
        super().set_data_in(data_in)

    def fit(self):
        self.cleaned_options = self._clean_solver_options()
        # self.proc.set_params(**cleaned_options)
        # self.proc.fit(self.X)
        return

    def transform(self,data):
        if config['min/max'] == 'max':
            data.append_data_column("X", pd.DataFrame(argmax(self.X)))
        else:
            data.append_data_column("X", pd.DataFrame(argmin(self.X)))
        return data