from vai_lab._plugin_templates import DataProcessingT
from sklearn.preprocessing import PolynomialFeatures as model
import pandas as pd

_PLUGIN_READABLE_NAMES = {"PolynomialFeatures": "default",
                          "polyfeat": "alias",
                          "polynomialfeatures": "alias"}    # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "Other"}                  # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"interaction_only": "bool",
                             "include_bias": "bool"}        # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                  # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X", "Y", "X_tst", 'Y_tst'}        # type:ignore


class PolynomialFeatures(DataProcessingT):
    """ 
    Generate polynomial and interaction features
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()