from sklearn.preprocessing import MinMaxScaler as model
from vai_lab._plugin_templates import DataProcessingT
import pandas as pd

_PLUGIN_READABLE_NAMES = {"MinMaxScaler":"default"}     # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "scaler"}             # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}             # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"feature_range": "tuple"}  # type:ignore
_PLUGIN_REQUIRED_DATA = {}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}      # type:ignore

class MinMaxScaler(DataProcessingT):
    """
    This estimator scales and translates each feature individually such that it\n
    is in the given range on the training set, e.g. between zero and one
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.proc = model()