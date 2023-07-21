from vai_lab._plugin_templates import DataProcessingT

import pandas as pd
from sklearn.preprocessing import Binarizer as model

_PLUGIN_READABLE_NAMES = {"Binarizer":"default","binarizer":"alias"}    # type:ignore  
_PLUGIN_MODULE_OPTIONS = {"Type": "encoder"}                            # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                             # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"threshold": "float"}                      # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}                      # type:ignore

class Binarizer(DataProcessingT):
    """
    Binarize data (set feature values to 0 or 1) according to a threshold
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()