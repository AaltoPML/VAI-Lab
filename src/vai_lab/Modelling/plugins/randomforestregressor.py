from vai_lab._plugin_templates import ModellingPluginT
from sklearn.ensemble import RandomForestRegressor as model

_PLUGIN_READABLE_NAMES = {"RandomForestRegressor": "default",
                          "RFRegressor": "alias",
                          "RFR": "alias"}               # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                          # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}              # type:ignore


class RandomForestRegressor(ModellingPluginT):
    """
    A random forest regression
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()