from sklearn.preprocessing import StandardScaler as model
from vai_lab._plugin_templates import DataProcessingT
import pandas as pd

_PLUGIN_READABLE_NAMES = {
    "StandardScaler": "default", "standardscaler": "alias"}     # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "scaler"}                     # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}                     # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"with_mean": "bool"}               # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X", "Y", "X_tst", 'Y_tst'}            # type:ignore


class StandardScaler(DataProcessingT):
    """
    Standardize features by removing the mean and scaling to unit variance
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()