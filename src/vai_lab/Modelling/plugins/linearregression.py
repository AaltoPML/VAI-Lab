from vai_lab._plugin_templates import ModellingPluginT
from sklearn.linear_model import LinearRegression as model

_PLUGIN_READABLE_NAMES = {"LinearRegression": "default",
                          "LR": "alias"}                    # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}             # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                              # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                              # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                          # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                  # type:ignore


class LinearRegression(ModellingPluginT):
    """
    Ordinary least squares Linear Regression
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()