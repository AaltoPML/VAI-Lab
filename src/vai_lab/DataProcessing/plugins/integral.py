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

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()

    def fit(self):
        return

    def transform(self,data):
        data.append_data_column("X", pd.DataFrame(self.proc(self.X)))
        return data