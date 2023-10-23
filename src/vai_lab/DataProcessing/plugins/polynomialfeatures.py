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