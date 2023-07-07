from sklearn.preprocessing import LabelEncoder as model
from vai_lab._plugin_templates import DataProcessingT
import pandas as pd

_PLUGIN_READABLE_NAMES = {"LabelEncoder":"default","LE":"alias"}    # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "encoder"}                        # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}                         # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                      # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                          # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X","Y","X_tst", 'Y_tst'}                  # type:ignore

class LabelEncoder(DataProcessingT):
    """
    Encode target labels with value between 0 and n_classes-1
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()