from vai_lab._plugin_templates import ModellingPluginT
from sklearn.neighbors import KNeighborsRegressor as model

_PLUGIN_READABLE_NAMES = {"KNNRegressor": "default",
                          "KNN-R": "alias"}             # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "regression"}         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"n_neighbors": "int",
                             "weights": "str"}          # type:ignore  
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {"X_tst", 'Y_tst'}              # type:ignore


class KNNRegressor(ModellingPluginT):
    """
    Regression based on k-nearest neighbors
    """

    def __init__(self):
        """Initialises parent class. 
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        self.model = model()