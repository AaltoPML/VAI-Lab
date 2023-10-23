from scipy.integrate import simps as model
from vai_lab._plugin_templates import DataProcessingT
import pandas as pd

_PLUGIN_READABLE_NAMES = {"Integral": "default",
                          "integral": "alias"}          # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "math operator"}      # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}             # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"dx": "float",
                             "axis": "int",
                             "even": "str"}             # type:ignore
_PLUGIN_REQUIRED_DATA = {}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst","Y_tst"}       # type:ignore

class Integral(DataProcessingT):
    """
    Calculate integral of array using the composite trapezoidal rule
    """

    def __init__(self, config = {}, data_in = [None]):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.set_data_in(data_in)
        self.configure(config)
        
        try:
            self.model = model(**self._config["options"])
        except Exception as exc:
            print('The plugin encountered an error on the parameters of '
                     +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
            raise
        
        self.fit_plugin = self.model.fit
        self.transform_plugin = self.model.transform

    def fit(self):
        return

    def transform(self,data):
        data.append_data_column("X", pd.DataFrame(self.proc(self.X)))
        return data