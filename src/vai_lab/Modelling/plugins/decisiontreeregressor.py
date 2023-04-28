from vai_lab._plugin_templates import ModellingPluginT
from sklearn.tree import DecisionTreeRegressor as model

_PLUGIN_READABLE_NAMES = {"DecisionTreeRegressor": "default",
                          "DTregressor": "alias"}               # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}                 # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"max_depth": "int"}                # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                              # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}                      # type:ignore


class DecisionTreeRegressor(ModellingPluginT):
    """
    A decision tree regressor
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.clf = model()