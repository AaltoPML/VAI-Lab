from sklearn.preprocessing import QuantileTransformer as model
from vai_lab._plugin_templates import DataProcessingT
import pandas as pd

_PLUGIN_READABLE_NAMES = {
    "QuantileTransformer": "default", "Quantile": "alias"}  # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "encoder"}                # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"Data": "str"}                 # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"n_quantiles": "int"}          # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X", "Y", "X_tst", 'Y_tst'}        # type:ignore


class QuantileTransformer(DataProcessingT):
    """
    Transform features using quantiles information
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()