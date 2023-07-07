from vai_lab._plugin_templates import DataProcessingT
from vai_lab._types import DataInterface

from sklearn.preprocessing import Normalizer as model
import pandas as pd

_PLUGIN_READABLE_NAMES = {"Normalizer": "default",
                          "Norm": "alias", "normalizer": "alias"}   # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "scaler"}                         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}                         # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                      # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                          # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X", "Y", "X_tst", 'Y_tst'}                # type:ignore


class Normalizer(DataProcessingT):
    """
    Normalize samples individually to unit norm
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()