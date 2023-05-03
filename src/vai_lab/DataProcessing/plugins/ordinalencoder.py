from sklearn.preprocessing import OrdinalEncoder as model
from vai_lab._plugin_templates import DataProcessingT
import pandas as pd

_PLUGIN_READABLE_NAMES = {"OrdinalEncoder": "default"}      # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "encoder"}                # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}                 # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"categories": "array-like"}    # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X", "Y", "X_tst", 'Y_tst'}        # type:ignore


class OrdinalEncoder(DataProcessingT):
    """
    Encode categorical features as an integer array
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.proc = model()